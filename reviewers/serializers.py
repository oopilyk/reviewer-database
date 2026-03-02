from rest_framework import serializers
from .models import Reviewer, ReviewerSubjectAreas, ReviewerHistory, Panel


class ReviewerListSerializer(serializers.ModelSerializer):
    """Lightweight for list views."""

    class Meta:
        model = Reviewer
        fields = [
            'id', 'fname', 'lname', 'email', 'status', 'panel_id',
            'mission', 'cycle', 'isChair', 'isDepChair', 'inst', 'Expertise_major', 'is_pinned',
        ]


class ReviewerDetailSerializer(serializers.ModelSerializer):
    """Full reviewer for retrieve/update."""
    conflicts_PI_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='conflicts_PI'
    )
    conflicts_CoI_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='conflicts_CoI'
    )
    conflicts_target_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='conflicts_target'
    )
    proposals_primary_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='proposals_primary'
    )
    proposals_secondary_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='proposals_secondary'
    )

    class Meta:
        model = Reviewer
        fields = '__all__'
        read_only_fields = ['id']


class ReviewerWriteSerializer(serializers.ModelSerializer):
    """For create/update (exclude heavy M2M from input)."""
    panel = serializers.PrimaryKeyRelatedField(queryset=Panel.objects.all())

    class Meta:
        model = Reviewer
        fields = [
            'fname', 'lname', 'email', 'user_id', 'status', 'panel',
            'mission', 'cycle', 'inst', 'inst2', 'Expertise_major', 'expertise_desc',
            'isChair', 'isDepChair', 'source', 'is_pinned', 'notes', 'url',
            'onNuSTARTeam', 'NuSTARProjectFunding', 'AtForeignInst',
        ]
