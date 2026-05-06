const router = createRouter({
    history: createWebHistory('/'),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/Game/Home.vue')
        }
    ]
})

export default router
