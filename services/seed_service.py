from werkzeug.security import generate_password_hash

from config import ADMIN_USERNAME, ADMIN_PASSWORD
from models import db, AdminUser, Subject, Level, DocumentType, Tag, Document, SiteSettings


def seed_initial_data():
    if AdminUser.query.count() == 0:
        admin = AdminUser(
            username=ADMIN_USERNAME,
            password_hash=generate_password_hash(ADMIN_PASSWORD)
        )
        db.session.add(admin)

    if SiteSettings.query.count() == 0:
        db.session.add(SiteSettings(site_name='Academy Najjah'))

    subjects = [
        ('Mathématiques', 'Ressources mathématiques', '📐', '#3b82f6'),
        ('Physique', 'Cours et exercices de physique', '⚛️', '#8b5cf6'),
        ('Français', 'Ressources de français', '📚', '#f59e0b'),
        ('Anglais', 'Vocabulaire et grammaire', '🌍', '#10b981'),
        ('Informatique', 'Algorithmique et technologies', '💻', '#06b6d4'),
        ('Sciences', 'Sciences naturelles et expérimentales', '🔬', '#22c55e'),
        ('Histoire', 'Civilisations et événements historiques', '🏛️', '#f97316'),
        ('Géographie', 'Territoires et espaces', '🌎', '#14b8a6'),
    ]

    for name, desc, icon, color in subjects:
        if not Subject.query.filter_by(name=name).first():
            db.session.add(Subject(name=name, description=desc, icon=icon, color=color))

    levels = [
        '7ème année', '8ème année', '9ème année', '1ère secondaire', '2ème secondaire',
        '3ème secondaire', '4ème secondaire', 'Baccalauréat'
    ]
    for level_name in levels:
        if not Level.query.filter_by(name=level_name).first():
            db.session.add(Level(name=level_name))

    document_types = [
        'Cours', 'Exercice', 'Correction', 'Examen', 'Devoir', 'Résumé', 'Série', 'Annale', 'Fiche', 'Autre'
    ]
    for type_name in document_types:
        if not DocumentType.query.filter_by(name=type_name).first():
            db.session.add(DocumentType(name=type_name))

    sample_tags = ['#Bac', '#Math', '#Algèbre', '#Examen', '#Physique', '#Français', '#Informatique']
    for tag_name in sample_tags:
        if not Tag.query.filter_by(name=tag_name).first():
            db.session.add(Tag(name=tag_name))

    # Create demo documents if none exist
    if Document.query.count() == 0:
        math = Subject.query.filter_by(name='Mathématiques').first()
        phys = Subject.query.filter_by(name='Physique').first()
        info = Subject.query.filter_by(name='Informatique').first()
        level9 = Level.query.filter_by(name='9ème année').first()
        bac = Level.query.filter_by(name='Baccalauréat').first()
        doc_type_course = DocumentType.query.filter_by(name='Cours').first()
        doc_type_exercice = DocumentType.query.filter_by(name='Exercice').first()
        doc_type_examen = DocumentType.query.filter_by(name='Examen').first()

        documents = [
            {
                'title': 'Cours de fonctions mathématiques',
                'description': 'Support de cours complet sur les fonctions linéaires et affines.',
                'filename': 'cours_fonctions.pdf',
                'original_filename': 'cours_fonctions.pdf',
                'file_type': 'pdf',
                'file_size': 120000,
                'school_year': '2026',
                'author': 'Prof. Idrissi',
                'subject_id': math.id if math else None,
                'level_id': level9.id if level9 else None,
                'document_type_id': doc_type_course.id if doc_type_course else None,
                'is_visible': True,
                'is_featured': True,
                'allow_download': True,
                'views': 245,
                'downloads': 64,
            },
            {
                'title': 'Série d’exercices de physique',
                'description': 'Exercices sur l’énergie, la force et le mouvement.',
                'filename': 'serie_physique.pdf',
                'original_filename': 'serie_physique.pdf',
                'file_type': 'pdf',
                'file_size': 145000,
                'school_year': '2025',
                'author': 'Prof. Benali',
                'subject_id': phys.id if phys else None,
                'level_id': bac.id if bac else None,
                'document_type_id': doc_type_exercice.id if doc_type_exercice else None,
                'is_visible': True,
                'is_featured': False,
                'allow_download': True,
                'views': 320,
                'downloads': 88,
            },
            {
                'title': 'Examen informatique 2025',
                'description': 'Examen de synthèse en informatique avec correction.',
                'filename': 'examen_info.pdf',
                'original_filename': 'examen_info.pdf',
                'file_type': 'pdf',
                'file_size': 135000,
                'school_year': '2025',
                'author': 'Prof. Hafid',
                'subject_id': info.id if info else None,
                'level_id': bac.id if bac else None,
                'document_type_id': doc_type_examen.id if doc_type_examen else None,
                'is_visible': True,
                'is_featured': True,
                'allow_download': True,
                'views': 510,
                'downloads': 130,
            },
        ]

        for item in documents:
            doc = Document(**item)
            db.session.add(doc)

    db.session.commit()
