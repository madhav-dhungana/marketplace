from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Create User Groups"
    groups = ['Admin','Batuwa','Guide']

    def handle(self, *args, **options):
        for item in self.groups:
            group, created = Group.objects.get_or_create(name=item)
            all_permissions = Permission.objects.all()
            if group.name == 'Admin':
                for perms in all_permissions:
                    group.permissions.add(perms.id)
        self.stdout.write(f"Created groups {self.groups}")
