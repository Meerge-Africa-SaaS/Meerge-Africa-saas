const statItems = document.querySelectorAll('.stats__item');

for (let i = 0; i < statItems.length; i++) {
    const statItem = statItems[i];
    const statPercentage = statItem.querySelector('.stat-percent').textContent;
    const statBar = statItem.querySelector('.stat-progress > .progress-bar');
    statBar?.setAttribute('style', `width: ${statPercentage}`);
}