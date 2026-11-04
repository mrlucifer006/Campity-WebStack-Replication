/**
 * Campus Task Management & Posting System - Interactive Client Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    // Theme preference persistence
    const savedTheme = localStorage.getItem('taskhub-theme') || 'default';
    if (savedTheme !== 'default') {
        document.body.className = `theme-${savedTheme}`;
    }

    // Dynamic Reward & Helper Stake Calculation in Task Creation Form
    const rewardInput = document.getElementById('reward');
    const stakePreview = document.getElementById('stake-preview');
    if (rewardInput && stakePreview) {
        rewardInput.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value) || 0;
            const requiredStake = Math.max(10, Math.floor(val * 0.1));
            stakePreview.textContent = `Helper Stake Requirement: ${requiredStake} Credits (10% lock refunded upon verified delivery)`;
        });
    }

    // Auto-dismiss alerts after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });

    // Action Confirmation prompts
    document.querySelectorAll('[data-confirm]').forEach(el => {
        el.addEventListener('click', (e) => {
            const message = el.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});

function switchTheme(themeName) {
    if (themeName === 'default') {
        document.body.className = '';
        localStorage.removeItem('taskhub-theme');
    } else {
        document.body.className = `theme-${themeName}`;
        localStorage.setItem('taskhub-theme', themeName);
    }
}
