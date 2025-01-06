# Generated by Django 5.1.4 on 2024-12-24 03:06

import django.db.models.deletion
import django.utils.timezone
import pgvector.django.vector
from django.db import migrations, models
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hebo_organizations", "0001_initial"),
        ("versions", "0001_initial"),
    ]

    operations = [
        VectorExtension(),
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, max_length=250, unique=True)),
                (
                    "content",
                    models.TextField(
                        help_text="Content in markdown format. Supports standard markdown syntax."
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_published", models.BooleanField(default=False)),
                (
                    "organization",
                    models.ForeignKey(
                        help_text="Organization this agent belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pages",
                        to="hebo_organizations.organization",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="knowledge.page",
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        help_text="The version this page belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pages",
                        to="versions.version",
                    ),
                ),
            ],
            options={
                "verbose_name": "Page",
                "verbose_name_plural": "Pages",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Part",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_line",
                    models.PositiveIntegerField(
                        help_text="Starting line number in the original content"
                    ),
                ),
                (
                    "end_line",
                    models.PositiveIntegerField(
                        help_text="Ending line number in the original content"
                    ),
                ),
                (
                    "content_hash",
                    models.CharField(
                        help_text="Hash of the original content section for tracking changes",
                        max_length=64,
                    ),
                ),
                (
                    "part_type",
                    models.CharField(
                        choices=[
                            ("behaviour", "Behaviour"),
                            ("scenario", "Scenario"),
                            ("example", "Example"),
                        ],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                (
                    "identifier",
                    models.CharField(
                        help_text="Unique identifier for this part within its page",
                        max_length=100,
                    ),
                ),
                (
                    "is_handover",
                    models.BooleanField(
                        default=False,
                        help_text="Special tag for downstream processing (valid only for scenarios and examples)",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "is_valid",
                    models.BooleanField(
                        default=True,
                        help_text="Indicates if the original content has changed and needs reprocessing",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts",
                        to="knowledge.page",
                    ),
                ),
            ],
            options={
                "ordering": ["start_line"],
            },
        ),
        migrations.CreateModel(
            name="Vector",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "embedding_model",
                    models.CharField(
                        choices=[
                            ("ada002", "text-embedding-ada-002"),
                            ("minilm", "all-MiniLM-L6-v2"),
                            ("mpnet", "all-mpnet-base-v2"),
                            ("bger", "bge-large-en"),
                        ],
                        help_text="Must match the embedding model in agent settings",
                        max_length=20,
                    ),
                ),
                ("vector", pgvector.django.vector.VectorField(dimensions=1536)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vectors",
                        to="knowledge.part",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="part",
            index=models.Index(
                fields=["page", "part_type", "is_valid"],
                name="knowledge_p_page_id_cbad77_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="part",
            constraint=models.UniqueConstraint(
                fields=("page", "identifier"), name="unique_part_identifier_per_page"
            ),
        ),
        migrations.AddIndex(
            model_name="vector",
            index=models.Index(
                fields=["part", "embedding_model"],
                name="knowledge_v_part_id_dbcb66_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="vector",
            constraint=models.UniqueConstraint(
                fields=("part", "embedding_model"),
                name="unique_vector_per_part_and_model",
            ),
        ),
    ]
