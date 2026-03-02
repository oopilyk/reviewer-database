from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Reviewer
from .serializers import ReviewerListSerializer, ReviewerDetailSerializer, ReviewerWriteSerializer


class ReviewerViewSet(viewsets.ModelViewSet):
    """
    List, create, retrieve, update, delete reviewers.
    Query params: panel_id, mission, cycle, status
    """
    queryset = Reviewer.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['fname', 'lname', 'email', 'inst']
    ordering_fields = ['lname', 'fname', 'id']
    ordering = ['lname']

    def get_queryset(self):
        qs = Reviewer.objects.all()
        panel_id = self.request.query_params.get('panel_id')
        mission = self.request.query_params.get('mission')
        cycle = self.request.query_params.get('cycle')
        status = self.request.query_params.get('status')
        if panel_id is not None:
            qs = qs.filter(panel_id=panel_id)
        if mission:
            qs = qs.filter(mission=mission)
        if cycle is not None:
            qs = qs.filter(cycle=cycle)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewerListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ReviewerWriteSerializer
        return ReviewerDetailSerializer

    @action(detail=True, methods=['get'])
    def conflicts(self, request, pk=None):
        """Get conflict proposal IDs for this reviewer."""
        reviewer = self.get_object()
        return Response({
            'PI': list(reviewer.conflicts_PI.values_list('record_id', flat=True)),
            'CoI': list(reviewer.conflicts_CoI.values_list('record_id', flat=True)),
            'inst': list(reviewer.conflicts_inst.values_list('record_id', flat=True)),
            'collab': list(reviewer.conflicts_collab.values_list('record_id', flat=True)),
            'other': list(reviewer.conflicts_other.values_list('record_id', flat=True)),
            'target': list(reviewer.conflicts_target.values_list('record_id', flat=True)),
        })

    @action(detail=True, methods=['get'])
    def proposals(self, request, pk=None):
        """Get assigned proposal IDs (primary and secondary)."""
        reviewer = self.get_object()
        return Response({
            'primary': list(reviewer.proposals_primary.values_list('record_id', flat=True)),
            'secondary': list(reviewer.proposals_secondary.values_list('record_id', flat=True)),
        })
