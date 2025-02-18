from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from ...models import (
    Project,
    Material,
    MaterialRequest,
    Faculty,
    Department,
    Speciality,
    TeamMember,
    ProjectImage,
    Plan,
    Phase,
    Task,
    Event,
)


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create basic entities
        faculty = Faculty.objects.create(
            arabic_name="كلية الهندسة",
            latin_name="Faculty of Engineering",
            abreviated_name="Eng",
        )

        department = Department.objects.create(
            arabic_name="قسم الحاسوب",
            latin_name="Computer Department",
            abreviated_name="CS",
        )

        speciality = Speciality.objects.create(
            arabic_name="هندسة البرمجيات",
            latin_name="Software Engineering",
            abreviated_name="SE",
        )

        # Create materials
        materials = []
        for i in range(5):
            material = Material.objects.create(
                name=f"Material {i+1}",
                description=f"Description for material {i+1}",
                model_number=f"MOD{i+1}",
                manufacturer=f"Manufacturer {i+1}",
                measurement_range="0-100",
                precision="High",
                power_requirements="220V",
                dimensions="10x20x30",
                weight="5kg",
                status="available",
            )
            materials.append(material)

        # Create projects and related data
        for i in range(10):
            # Create project
            start_date = timezone.now().date()
            deadline = start_date + timedelta(days=random.randint(30, 180))

            project = Project.objects.create(
                name=f"Project {i+1}",
                description=f"Description for project {i+1}",
                progress=random.randint(0, 100),
                start_date=start_date,
                deadline=deadline,
                status=random.choice(
                    ["pending", "in_progress", "completed", "labeled"]
                ),
                logo="default_image_placeholder.png",
            )

            # Create project image
            ProjectImage.objects.create(
                project=project, image="default_image_placeholder.png"
            )

            # Create team members
            user = User.objects.create_user(
                username=f"user{i+1}",
                password="password123",
                first_name=f"First{i+1}",
                last_name=f"Last{i+1}",
            )

            TeamMember.objects.create(
                project=project,
                user=user,
                is_permitted_to_demand=True,
                is_project_leader=(i == 0),  # First user is project leader
                photo="default_image_placeholder.png",
                phone=f"+1234567890{i}",
                bio=f"Bio for team member {i+1}",
                role="supervisor" if i < 2 else "member",
                gender=random.choice(["male", "female"]),
                faculty=faculty,
                department=department,
                speciality=speciality,
            )

            # Create material requests
            MaterialRequest.objects.create(
                material=random.choice(materials),
                project=project,
                quantity=random.randint(1, 5),
                from_date=start_date,
                to_date=deadline,
            )

            # Create plan and phases
            plan = Plan.objects.create(project=project)

            for j in range(3):  # 3 phases per project
                phase = Phase.objects.create(
                    plan=plan,
                    title=f"Phase {j+1} of Project {i+1}",
                    deadline=start_date + timedelta(days=30 * (j + 1)),
                )

                # Create tasks for each phase
                for k in range(2):  # 2 tasks per phase
                    task = Task.objects.create(
                        name=f"Task {k+1} of Phase {j+1}",
                        description=f"Description for task {k+1}",
                        phase=phase,
                    )

                    # Create events for each task
                    Event.objects.create(
                        name=f"Event for Task {k+1}",
                        date=start_date + timedelta(days=random.randint(1, 30)),
                        description=f"Event description for task {k+1}",
                        task=task,
                    )

        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))
