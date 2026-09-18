import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from sqlalchemy import func

from models import db, AdminUser, Document, Subject, Level, DocumentType, Tag, SiteSettings
from services.document_service import build_safe_filename, validate_upload
from config import ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH

admin_bp = Blueprint('admin', __name__)


def admin_required(view):
    def wrapped(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('auth.admin_login'))
        return view(*args, **kwargs)
    wrapped.__name__ = view.__name__
    return wrapped


@admin_bp.route('/')
@admin_required
def dashboard():
    total_documents = Document.query.count()
    visible_documents = Document.query.filter_by(is_visible=True).count()
    hidden_documents = Document.query.filter_by(is_visible=False).count()
    total_categories = Subject.query.count()
    total_downloads = db.session.query(func.sum(Document.downloads)).scalar() or 0
    total_views = db.session.query(func.sum(Document.views)).scalar() or 0
    recent_documents = Document.query.order_by(Document.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_documents=total_documents,
                           visible_documents=visible_documents,
                           hidden_documents=hidden_documents,
                           total_categories=total_categories,
                           total_downloads=total_downloads,
                           total_views=total_views,
                           recent_documents=recent_documents)


@admin_bp.route('/documents')
@admin_required
def documents():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    documents_query = Document.query
    if q:
        documents_query = documents_query.filter(Document.title.ilike(f'%{q}%'))

    pagination = documents_query.order_by(Document.created_at.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template('admin/documents.html', pagination=pagination, q=q)


@admin_bp.route('/documents/new', methods=['GET', 'POST'])
@admin_required
def add_document():
    subjects = Subject.query.order_by(Subject.name).all()
    levels = Level.query.order_by(Level.name).all()
    document_types = DocumentType.query.order_by(DocumentType.name).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        subject_id = request.form.get('subject_id', type=int)
        level_id = request.form.get('level_id', type=int)
        document_type_id = request.form.get('document_type_id', type=int)
        school_year = request.form.get('school_year', '').strip()
        author = request.form.get('author', '').strip()
        tags = request.form.get('tags', '').strip()
        is_visible = request.form.get('is_visible') == 'on'
        is_featured = request.form.get('is_featured') == 'on'
        allow_download = request.form.get('allow_download') == 'on'
        is_pinned = request.form.get('is_pinned') == 'on'
        file = request.files.get('file')

        if not title:
            flash('Le titre est requis.', 'danger')
            return render_template('admin/upload.html', subjects=subjects, levels=levels, document_types=document_types)

        valid, result = validate_upload(file)
        if not valid:
            flash(result, 'danger')
            return render_template('admin/upload.html', subjects=subjects, levels=levels, document_types=document_types)

        if file and hasattr(file, 'stream'):
            file.stream.seek(0)

        safe_name = build_safe_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_name)
        file.save(file_path)

        document = Document(
            title=title,
            description=description,
            filename=safe_name,
            original_filename=file.filename,
            file_type=result['extension'],
            file_size=result['size'],
            subject_id=subject_id,
            level_id=level_id,
            document_type_id=document_type_id,
            school_year=school_year,
            author=author,
            is_visible=is_visible,
            is_featured=is_featured,
            allow_download=allow_download,
            is_pinned=is_pinned,
        )
        db.session.add(document)
        db.session.flush()

        if tags:
            for tag_name in [t.strip() for t in tags.split(',') if t.strip()]:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()
                document.tags.append(tag)

        db.session.commit()
        flash('Document ajouté avec succès.', 'success')
        return redirect(url_for('admin.documents'))

    return render_template('admin/upload.html', subjects=subjects, levels=levels, document_types=document_types)


@admin_bp.route('/documents/<int:document_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_document(document_id):
    document = Document.query.get_or_404(document_id)
    subjects = Subject.query.order_by(Subject.name).all()
    levels = Level.query.order_by(Level.name).all()
    document_types = DocumentType.query.order_by(DocumentType.name).all()

    if request.method == 'POST':
        document.title = request.form.get('title', document.title).strip()
        document.description = request.form.get('description', document.description).strip()
        document.subject_id = request.form.get('subject_id', type=int) or document.subject_id
        document.level_id = request.form.get('level_id', type=int) or document.level_id
        document.document_type_id = request.form.get('document_type_id', type=int) or document.document_type_id
        document.school_year = request.form.get('school_year', document.school_year).strip()
        document.author = request.form.get('author', document.author).strip()
        document.is_visible = request.form.get('is_visible') == 'on'
        document.is_featured = request.form.get('is_featured') == 'on'
        document.allow_download = request.form.get('allow_download') == 'on'
        document.is_pinned = request.form.get('is_pinned') == 'on'

        tags_input = request.form.get('tags', '')
        document.tags.clear()
        if tags_input:
            for tag_name in [t.strip() for t in tags_input.split(',') if t.strip()]:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()
                document.tags.append(tag)

        file = request.files.get('file')
        if file and file.filename:
            valid, result = validate_upload(file)
            if not valid:
                flash(result, 'danger')
            else:
                if hasattr(file, 'stream'):
                    file.stream.seek(0)
                safe_name = build_safe_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_name)
                file.save(file_path)
                document.filename = safe_name
                document.original_filename = file.filename
                document.file_type = result['extension']
                document.file_size = result['size']

        db.session.commit()
        flash('Document modifié avec succès.', 'success')
        return redirect(url_for('admin.documents'))

    return render_template('admin/edit_document.html', document=document, subjects=subjects, levels=levels, document_types=document_types)


@admin_bp.route('/documents/<int:document_id>/delete', methods=['POST'])
@admin_required
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    db.session.delete(document)
    db.session.commit()
    flash('Document supprimé.', 'success')
    return redirect(url_for('admin.documents'))


@admin_bp.route('/categories')
@admin_required
def categories():
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('admin/categories.html', subjects=subjects)


@admin_bp.route('/categories/new', methods=['POST'])
@admin_required
def add_category():
    name = request.form.get('name', '').strip()
    if name:
        if not Subject.query.filter_by(name=name).first():
            subject = Subject(name=name, description=request.form.get('description', ''), icon=request.form.get('icon', '📚'))
            db.session.add(subject)
            db.session.commit()
            flash('Catégorie ajoutée.', 'success')
        else:
            flash('Cette catégorie existe déjà.', 'warning')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/levels')
@admin_required
def levels():
    levels = Level.query.order_by(Level.name).all()
    return render_template('admin/levels.html', levels=levels)


@admin_bp.route('/levels/new', methods=['POST'])
@admin_required
def add_level():
    name = request.form.get('name', '').strip()
    if name and not Level.query.filter_by(name=name).first():
        db.session.add(Level(name=name, description=request.form.get('description', '')))
        db.session.commit()
        flash('Niveau ajouté.', 'success')
    return redirect(url_for('admin.levels'))


@admin_bp.route('/settings')
@admin_required
def settings():
    site_settings = SiteSettings.query.first() or SiteSettings()
    return render_template('admin/settings.html', site_settings=site_settings)


@admin_bp.route('/settings', methods=['POST'])
@admin_required
def save_settings():
    site_settings = SiteSettings.query.first() or SiteSettings()
    site_settings.site_name = request.form.get('site_name', site_settings.site_name)
    site_settings.site_description = request.form.get('site_description', site_settings.site_description)
    site_settings.contact_email = request.form.get('contact_email', site_settings.contact_email)
    site_settings.documents_per_page = int(request.form.get('documents_per_page', site_settings.documents_per_page))
    site_settings.max_upload_size = int(request.form.get('max_upload_size', site_settings.max_upload_size))
    site_settings.download_enabled = request.form.get('download_enabled') == 'on'
    site_settings.maintenance_mode = request.form.get('maintenance_mode') == 'on'
    db.session.add(site_settings)
    db.session.commit()
    flash('Paramètres sauvegardés.', 'success')
    return redirect(url_for('admin.settings'))
