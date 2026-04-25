from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task, Comment, Notification
from .serializers import TaskSerializer, CommentSerializer, NotificationSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Task.objects.filter(team__members=self.request.user)
    
    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        Notification.objects.create(
            user=task.assigned_to,
            message=f'New task assigned: {task.title}',
            related_task=task
        )

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_id'])
    
    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        comment = serializer.save(user=self.request.user, task=task)
        if comment.user != task.assigned_to:
            Notification.objects.create(
                user=task.assigned_to,
                message=f'{self.request.user.username} commented on "{task.title}"',
                related_task=task
            )

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationMarkReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})
