from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'employee':
            return Task.objects.filter(user=user)  # Employee sees own tasks
        elif user.role == 'manager':
            return Task.objects.all()  # Manager sees all tasks
        return Task.objects.none()  # No access for others

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status == 'approved':
            return Response(
                {'error': 'Approved tasks cannot be edited.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status == 'approved':
            return Response(
                {'error': 'Approved tasks cannot be deleted.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        task = self.get_object()
        if request.user.role != 'manager':
            return Response({'error': 'Only managers can approve tasks.'}, status=403)

        if task.status == 'approved':
            return Response({'message': 'Task is already approved.'}, status=400)

        task.status = 'approved'
        task.manager_comment = request.data.get('comment', '')
        task.save()
        return Response({'status': 'Task Approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        task = self.get_object()
        if request.user.role != 'manager':
            return Response({'error': 'Only managers can reject tasks.'}, status=403)

        if task.status == 'rejected':
            return Response({'message': 'Task is already rejected.'}, status=400)

        task.status = 'rejected'
        task.manager_comment = request.data.get('comment', '')
        task.save()
        return Response({'status': 'Task Rejected'})
