import { createApp } from 'vue';
import App from './App.vue';

// Import Vuetify and styles
import 'vuetify/styles'; // Import Vuetify CSS styles
import { createVuetify } from 'vuetify';

// Create Vuetify instance
const vuetify = createVuetify();

// Create Vue app and use Vuetify
createApp(App)
  .use(vuetify)
  .mount('#app');