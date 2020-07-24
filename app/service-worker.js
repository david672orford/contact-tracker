importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

if(!workbox) {
	console.error('sw: Workbox failed to load');
} else {
	console.log('sw: Workbox loaded');

	const {registerRoute} = workbox.routing;
	const {CacheFirst} = workbox.strategies;

	registerRoute(
		({url}) => url.origin === self.location.origin && url.pathname.startsWith('/static/'),
			new CacheFirst({
				cacheName: 'static'
				})
		);

	/* This would not work correctly because this page changes
	   in response to button presses. We'll leave this disabled
	   until that can be changed. */
	//const {setDefaultHandler} = workbox.routing;
	//const {StaleWhileRevalidate} = workbox.strategies;
	//const {BroadcastUpdatePlugin} = workbox.broadcastUpdate;
	//setDefaultHandler(
	//	new StaleWhileRevalidate({
	//		cacheName: 'main',
	//		plugins: [new BroadcastUpdatePlugin()]
	//		})
	//	);

}
