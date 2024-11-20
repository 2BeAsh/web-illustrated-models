<template>
  <v-container>
    <h1>Parameter Input</h1>
    
    <v-row>
      <v-col cols="12">
        <v-slider
          v-model="parameters.a"
          :min="0"
          :max="100"
          step="1"
          label="Parameter A"
        ></v-slider>
      </v-col>

      <v-col cols="12">
        <v-slider
          v-model="parameters.b"
          :min="0"
          :max="100"
          step="1"
          label="Parameter B"
        ></v-slider>
      </v-col>
    </v-row>

    <v-btn @click="sendData" color="primary" :loading="loading">
      Run Model
    </v-btn>

    <div v-if="result">
      <h2>Model Result:</h2>
      <pre>{{ result }}</pre>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      parameters: { a: 0, b: 0 },
      result: null,
      loading: false,
    };
  },
  methods: {
    async sendData() {
      this.loading = true;
      try {
        const response = await axios.post("http://127.0.0.1:5000/api/model", {
          parameters: this.parameters,
        });
        this.result = response.data.result;
      } catch (error) {
        console.error("Error:", error);
        alert("There was an error processing your request.");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Custom styles for your component */
label {
  display: block;
  margin: 10px 0;
}
</style>