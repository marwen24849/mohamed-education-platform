from . import db


class SiteSettings(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(120), default='EduVault')
    site_description = db.Column(db.Text, default='Plateforme éducative moderne')
    contact_email = db.Column(db.String(120), default='contact@eduvault.local')
    documents_per_page = db.Column(db.Integer, default=12)
    max_upload_size = db.Column(db.Integer, default=15 * 1024 * 1024)
    download_enabled = db.Column(db.Boolean, default=True)
    maintenance_mode = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<SiteSettings {self.site_name}>'
