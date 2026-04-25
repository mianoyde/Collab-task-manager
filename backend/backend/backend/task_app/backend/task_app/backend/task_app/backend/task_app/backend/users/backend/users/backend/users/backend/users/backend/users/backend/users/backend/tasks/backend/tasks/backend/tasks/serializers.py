
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Task
        fields = '_all_'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Comment
        fields = '_all_'
        read_only_fields = ('user', 'created_at')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '_all_'
        read_only_fields = ('user', 'created_at')
