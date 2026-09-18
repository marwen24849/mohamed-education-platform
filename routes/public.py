from flask import Blueprint, render_template, request, redirect, abort, send_from_directory, session
from sqlalchemy import or_

from models import Document, Subject, Level, DocumentType, SiteSettings, db

public_bp = Blueprint('public', __name__)


@public_bp.context_processor
def inject_global_context():
    settings = SiteSettings.query.first() or SiteSettings()
    return {
        'site_settings': settings,
        'subjects': Subject.query.order_by(Subject.name).all(),
        'levels': Level.query.order_by(Level.name).all(),
        'document_types': DocumentType.query.order_by(DocumentType.name).all(),
    }


@public_bp.before_request
def check_maintenance_mode():
    settings = SiteSettings.query.first()
    if settings and settings.maintenance_mode and request.endpoint not in {'auth.admin_login', 'auth.admin_logout', 'admin.dashboard', 'admin.documents', 'admin.add_document', 'admin.edit_document', 'admin.delete_document', 'admin.categories', 'admin.add_category', 'admin.levels', 'admin.add_level', 'admin.settings', 'admin.save_settings', 'public.maintenance'}:
        if not session.get('admin_logged_in'):
            return redirect('/maintenance')


@public_bp.route('/')
def index():
    featured = Document.query.filter_by(is_visible=True, is_featured=True).order_by(Document.created_at.desc()).limit(4).all()
    recent = Document.query.filter_by(is_visible=True).order_by(Document.created_at.desc()).limit(6).all()
    popular = Document.query.filter_by(is_visible=True).order_by(Document.views.desc(), Document.downloads.desc()).limit(6).all()
    total_documents = Document.query.count()
    total_views = db.session.query(db.func.sum(Document.views)).scalar() or 0
    total_downloads = db.session.query(db.func.sum(Document.downloads)).scalar() or 0
    return render_template('index.html', featured=featured, recent=recent, popular=popular,
                           total_documents=total_documents, total_views=total_views, total_downloads=total_downloads)


@public_bp.route('/documents')
def documents_page():
    subject_id = request.args.get('subject_id', type=int)
    level_id = request.args.get('level_id', type=int)
    document_type_id = request.args.get('document_type_id', type=int)
    q = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'recent')
    page = request.args.get('page', 1, type=int)

    query = Document.query.filter_by(is_visible=True)
    if subject_id:
        query = query.filter_by(subject_id=subject_id)
    if level_id:
        query = query.filter_by(level_id=level_id)
    if document_type_id:
        query = query.filter_by(document_type_id=document_type_id)
    if q:
        query = query.filter(
            or_(
                Document.title.ilike(f'%{q}%'),
                Document.description.ilike(f'%{q}%'),
                Document.author.ilike(f'%{q}%'),
                Document.school_year.ilike(f'%{q}%')
            )
        )

    if sort == 'popular':
        query = query.order_by(Document.views.desc(), Document.downloads.desc())
    elif sort == 'downloads':
        query = query.order_by(Document.downloads.desc())
    elif sort == 'alphabetical':
        query = query.order_by(Document.title.asc())
    else:
        query = query.order_by(Document.created_at.desc())

    pagination = query.paginate(page=page, per_page=12, error_out=False)
    return render_template('documents.html', pagination=pagination, q=q, subject_id=subject_id, level_id=level_id, document_type_id=document_type_id, sort=sort)


@public_bp.route('/document/<int:document_id>')
def document_detail(document_id):
    document = Document.query.get_or_404(document_id)
    if not document.is_visible:
        abort(404)

    document.views += 1
    db.session.commit()

    prev_doc = Document.query.filter(Document.id < document_id, Document.is_visible == True).order_by(Document.id.desc()).first()
    next_doc = Document.query.filter(Document.id > document_id, Document.is_visible == True).order_by(Document.id.asc()).first()
    return render_template('document_detail.html', document=document, prev_doc=prev_doc, next_doc=next_doc)


@public_bp.route('/document/<int:document_id>/preview')
def preview_document(document_id):
    document = Document.query.get_or_404(document_id)
    if not document.is_visible:
        abort(404)

    return send_from_directory('uploads', document.filename, as_attachment=False)


@public_bp.route('/download/<int:document_id>')
def download_document(document_id):
    document = Document.query.get_or_404(document_id)
    if not document.is_visible or not document.allow_download:
        abort(403)

    document.downloads += 1
    db.session.commit()
    return send_from_directory('uploads', document.filename, as_attachment=True, download_name=document.original_filename)


@public_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return render_template('search.html', results=[], query='')

    term = f'%{q}%'
    results = Document.query.filter_by(is_visible=True).filter(
        (Document.title.ilike(term)) |
        (Document.description.ilike(term)) |
        (Document.school_year.ilike(term)) |
        (Document.author.ilike(term))
    ).order_by(Document.created_at.desc()).all()
    return render_template('search.html', results=results, query=q)


@public_bp.route('/subjects')
def subjects_page():
    all_subjects = Subject.query.order_by(Subject.name).all()
    return render_template('subjects.html', subjects=all_subjects)


@public_bp.route('/subjects/<int:subject_id>')
def subject_detail(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    docs = Document.query.filter_by(subject_id=subject_id, is_visible=True).order_by(Document.created_at.desc()).all()
    return render_template('subject_detail.html', subject=subject, documents=docs)


@public_bp.route('/levels')
def levels_page():
    all_levels = Level.query.order_by(Level.name).all()
    return render_template('levels.html', levels=all_levels)


@public_bp.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')


@public_bp.route('/favicon.ico')
def favicon():
    return redirect('/static/images/favicon.svg')
