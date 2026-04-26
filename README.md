# Collab-task-manager
Collab task management web app
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
    const [tasks, setTasks] = useState([]);
    const [teams, setTeams] = useState([]);
    const [notifications, setNotifications] = useState([]);
    const [showNotifications, setShowNotifications] = useState(false);
    const [newTask, setNewTask] = useState({ 
        title: '', 
        description: '', 
        deadline: '', 
        priority: 'MED',
        assigned_to: '',
        team: ''
    });
    const [newTeam, setNewTeam] = useState({ name: '', member_ids: [] });
    const [selectedTask, setSelectedTask] = useState(null);
    const [newComment, setNewComment] = useState('');
    const username = localStorage.getItem('username');
    const userId = localStorage.getItem('user_id');

    const api = axios.create({
        baseURL: 'http://localhost:8000/api',
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
    });

    useEffect(() => {
        fetchTasks();
        fetchTeams();
        fetchNotifications();
        
        // Poll for new notifications every 5 seconds
        const interval = setInterval(fetchNotifications, 5000);
        return () => clearInterval(interval);
    }, []);

    const fetchTasks = async () => {
        try {
            const res = await api.get('/tasks/');
            setTasks(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    const fetchTeams = async () => {
        try {
            const res = await api.get('/teams/');
            setTeams(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    const fetchNotifications = async () => {
        try {
            const res = await api.get('/notifications/');
            setNotifications(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    const markNotificationRead = async (id) => {
        try {
            await api.patch(`/notifications/${id}/read/`);
            fetchNotifications();
        } catch (error) {
            console.error(error);
        }
    };

    const createTask = async (e) => {
        e.preventDefault();
        try {
            await api.post('/tasks/', newTask);
            setNewTask({ title: '', description: '', deadline: '', priority: 'MED', assigned_to: '', team: '' });
            fetchTasks();
        } catch (error) {
            alert('Error creating task');
        }
    };

    const createTeam = async (e) => {
        e.preventDefault();
        try {
            await api.post('/teams/', { name: newTeam.name, member_ids: newTeam.member_ids });
            setNewTeam({ name: '', member_ids: [] });
            fetchTeams();
        } catch (error) {
            alert('Error creating team');
        }
    };

    const updateTaskStatus = async (taskId, newStatus) => {
        try {
            await api.patch(`/tasks/${taskId}/`, { status: newStatus });
            fetchTasks();
        } catch (error) {
            console.error(error);
        }
    };

    const addComment = async () => {
        if (!newComment.trim() || !selectedTask) return;
        try {
            await api.post(`/tasks/${selectedTask.id}/comments/`, { content: newComment });
            setNewComment('');
            // Refresh task details
            const res = await api.get(`/tasks/${selectedTask.id}/`);
            setSelectedTask(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    const logout = () => {
        localStorage.clear();
        window.location.href = '/login';
    };

    const unreadCount = notifications.filter(n => !n.is_read).length;

    return (
        <div style={{ padding: 20 }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h1>Welcome, {username}!</h1>
                <div style={{ position: 'relative' }}>
                    <button onClick={() => setShowNotifications(!showNotifications)}>
                        🔔 {unreadCount > 0 && `(${unreadCount})`}
                    </button>
                    {showNotifications && (
                        <div style={{ position: 'absolute', right: 0, top: 30, background: 'white', border: '1px solid #ccc', width: 300, maxHeight: 400, overflow: 'auto', zIndex: 1000 }}>
                            {notifications.length === 0 ? (
                                <p style={{ padding: 10 }}>No notifications</p>
                            ) : (
                                notifications.map(notif => (
                                    <div key={notif.id} style={{ padding: 10, borderBottom: '1px solid #eee', background: notif.is_read ? 'white' : '#f0f0f0' }} onClick={() => markNotificationRead(notif.id)}>
                                        {notif.message}
                                        <small style={{ display: 'block', fontSize: 10 }}>{new Date(notif.created_at).toLocaleString()}</small>
                                    </div>
                                ))
                            )}
                        </div>
                    )}
                    <button onClick={logout} style={{ marginLeft: 10 }}>Logout</button>
                </div>
            </div>

            {/* Create Team Section */}
            <div style={{ border: '1px solid #ccc', padding: 15, margin: '20px 0' }}>
                <h3>Create Team</h3>
                <form onSubmit={createTeam}>
                    <input placeholder="Team Name" value={newTeam.name} onChange={(e) => setNewTeam({ ...newTeam, name: e.target.value })} required />
                    <button type="submit">Create Team</button>
                </form>
            </div>

            {/* Create Task Section */}
            <div style={{ border: '1px solid #ccc', padding: 15, margin: '20px 0' }}>
                <h3>Create Task</h3>
                <form onSubmit={createTask}>
                    <input placeholder="Title" value={newTask.title} onChange={(e) => setNewTask({ ...newTask, title: e.target.value })} required /><br/>
                    <textarea placeholder="Description" value={newTask.description} onChange={(e) => setNewTask({ ...newTask, description: e.target.value })} /><br/>
                    <input type="datetime-local" value={newTask.deadline} onChange={(e) => setNewTask({ ...newTask, deadline: e.target.value })} required /><br/>
                    <select value={newTask.priority} onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}>
                        <option value="LOW">Low</option>
                        <option value="MED">Medium</option>
                        <option value="HIGH">High</option>
                    </select><br/>
                    <select value={newTask.assigned_to} onChange={(e) => setNewTask({ ...newTask, assigned_to: e.target.value })} required>
                        <option value="">Assign to user</option>
                        {/* You'd populate this with users from API */}
                    </select><br/>
                    <select value={newTask.team} onChange={(e) => setNewTask({ ...newTask, team: e.target.value })} required>
                        <option value="">Select Team</option>
                        {teams.map(team => (
                            <option key={team.id} value={team.id}>{team.name}</option>
                        ))}
                    </select><br/>
                    <button type="submit">Create Task</button>
                </form>
            </div>

            {/* Task List */}
            <h2>Your Tasks</h2>
            <div style={{ display: 'grid', gap: 10 }}>
                {tasks.map(task => (
                    <div key={task.id} style={{ border: '1px solid #ccc', padding: 10, cursor: 'pointer' }} onClick={() => setSelectedTask(task)}>
                        <h3>{task.title}</h3>
                        <p>Priority: {task.priority} | Status: {task.status} | Deadline: {new Date(task.deadline).toLocaleString()}</p>
                        <div>
                            <button onClick={(e) => { e.stopPropagation(); updateTaskStatus(task.id, 'TODO'); }}>Todo</button>
                            <button onClick={(e) => { e.stopPropagation(); updateTaskStatus(task.id, 'INPROG'); }}>In Progress</button>
                            <button onClick={(e) => { e.stopPropagation(); updateTaskStatus(task.id, 'DONE'); }}>Done</button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Task Detail Modal */}
            {selectedTask && (
                <div style={{ position: 'fixed', top: '10%', left: '30%', width: '40%', background: 'white', border: '2px solid #000', padding: 20, zIndex: 1001 }}>
                    <h2>{selectedTask.title}</h2>
                    <p>{selectedTask.description}</p>
                    <p>Priority: {selectedTask.priority}</p>
                    <p>Status: {selectedTask.status}</p>
                    <p>Deadline: {new Date(selectedTask.deadline).toLocaleString()}</p>
                    
                    <h3>Comments</h3>
                    <div style={{ maxHeight: 200, overflow: 'auto' }}>
                        {selectedTask.comments?.map(comment => (
                            <div key={comment.id} style={{ borderBottom: '1px solid #eee', margin: 5, padding: 5 }}>
                                <strong>{comment.user_detail?.username}:</strong> {comment.content}
                                <small>{new Date(comment.created_at).toLocaleString()}</small>
                            </div>
                        ))}
                    </div>
                    
                    <textarea value={newComment} onChange={(e) => setNewComment(e.target.value)} placeholder="Add a comment..." style={{ width: '100%', margin: '10px 0' }} />
                    <button onClick={addComment}>Post Comment</button>
                    <button onClick={() => setSelectedTask(null)} style={{ marginLeft: 10 }}>Close</button>
                </div>
            )}
        </div>
    );
}




