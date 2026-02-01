// Service Worker para Red Social PWA
// Versión del cache
const CACHE_NAME = 'red-social-v1';
const RUNTIME_CACHE = 'red-social-runtime-v1';

// Archivos estáticos para cachear al instalar
const STATIC_CACHE_URLS = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/uploads/default_avatar.png',
  '/login',
  '/register'
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Cacheando archivos estáticos');
        return cache.addAll(STATIC_CACHE_URLS.map(url => {
          try {
            return new Request(url);
          } catch (e) {
            return url;
          }
        }));
      })
      .then(() => {
        return self.skipWaiting();
      })
      .catch((error) => {
        console.log('[Service Worker] Error al cachear:', error);
      })
  );
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activando...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => {
            return cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE;
          })
          .map((cacheName) => {
            console.log('[Service Worker] Eliminando cache antiguo:', cacheName);
            return caches.delete(cacheName);
          })
      );
    })
    .then(() => {
      return self.clients.claim();
    })
  );
});

// Interceptar peticiones (estrategia Cache First con fallback a Network)
self.addEventListener('fetch', (event) => {
  // No cachear peticiones de API o POST/PUT/DELETE
  if (event.request.method !== 'GET') {
    return;
  }

  // No cachear peticiones a rutas de API
  if (event.request.url.includes('/api/') || 
      event.request.url.includes('/post/') && !event.request.url.includes('/static/')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // Si está en cache, devolverlo
        if (cachedResponse) {
          return cachedResponse;
        }

        // Si no está en cache, hacer petición a la red
        return fetch(event.request)
          .then((response) => {
            // No cachear respuestas que no sean exitosas
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clonar la respuesta para cachearla
            const responseToCache = response.clone();

            // Cachear respuestas de archivos estáticos
            if (event.request.url.includes('/static/')) {
              caches.open(RUNTIME_CACHE)
                .then((cache) => {
                  cache.put(event.request, responseToCache);
                });
            }

            return response;
          })
          .catch(() => {
            // Si falla la red, intentar devolver página offline o cache
            if (event.request.destination === 'document') {
              return caches.match('/').then((response) => {
                return response || new Response('Sin conexión', {
                  status: 503,
                  headers: { 'Content-Type': 'text/html' }
                });
              });
            }
            // Para otros recursos, intentar devolver del cache
            return caches.match(event.request);
          });
      })
  );
});

// Manejo de mensajes desde la app
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Sincronización en segundo plano (para futuras mejoras)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-posts') {
    console.log('[Service Worker] Sincronizando posts...');
    // Aquí se podría implementar sincronización de datos
  }
});
