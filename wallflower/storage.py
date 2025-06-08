from django.core.files.storage import FileSystemStorage

class NoLockFileSystemStorage(FileSystemStorage):
    def _save(self, name, content):
        # Skip file locking (causes Termux errors)
        return super()._save(name, content)