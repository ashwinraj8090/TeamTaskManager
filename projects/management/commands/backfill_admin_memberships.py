from django.core.management.base import BaseCommand
from projects.models import Project, Membership


class Command(BaseCommand):
    help = 'Backfill ADMIN Membership entries for existing projects whose owner has no membership.'

    def handle(self, *args, **options):
        projects = Project.objects.all()
        created_count = 0
        skipped_count = 0

        for project in projects:
            membership, created = Membership.objects.get_or_create(
                user=project.owner,
                project=project,
                defaults={'role': Membership.ADMIN}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [OK] Created ADMIN membership: {project.owner.email} -> "{project.title}"'
                    )
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    f'  [SKIP] Already exists: {project.owner.email} -> "{project.title}" (role={membership.role})'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone. {created_count} membership(s) created, {skipped_count} already existed.'
            )
        )
