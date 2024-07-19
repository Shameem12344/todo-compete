// Add your custom JavaScript here
document.addEventListener('DOMContentLoaded', function() {
    // Example: Add animation to completed tasks
    const completedTasks = document.querySelectorAll('.badge-success');
    completedTasks.forEach(task => {
        task.style.transition = 'all 0.3s';
        task.addEventListener('mouseover', () => {
            task.style.transform = 'scale(1.1)';
        });
        task.addEventListener('mouseout', () => {
            task.style.transform = 'scale(1)';
        });
    });
});

