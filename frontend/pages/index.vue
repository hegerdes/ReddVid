<template>
  <v-app dark>
    <v-main>
      <v-container>
        <v-row justify="center" align="center">
          <v-col cols="12">
            <v-card class="logo py-4 d-flex justify-center">
              <v-img src="reddvid_small.png" height="350" />
            </v-card>
            <v-card>
              <v-card-title class="headline">
                ReddVid - Easy way to download Videos from Reddit!
              </v-card-title>
              <v-card-text>
                <p>Past the Post URL here:</p>
              </v-card-text>
              <v-form ref="form" lazy-validation>
                <v-text-field v-model="url" label="Post URL" required />
              </v-form>
              <div v-if="running">
                <v-progress-linear indeterminate />
              </div>
              <v-card-actions>
                <v-spacer />
                <v-btn @click="genereteDownloadURL" color="primary">
                  Continue
                </v-btn>
                <v-spacer />
              </v-card-actions>
              <div v-if="video_found">
                <v-card-text>
                  <p>Video Found! Download here:</p>
                </v-card-text>
                <v-card-actions>
                  <v-spacer />
                  <v-btn @click="DownloadVid" color="primary"> Download </v-btn>
                  <v-spacer />
                </v-card-actions>
              </div>
              <v-card-text v-if="error">
                <p>Error!</p>
                <p>Please check the provided URL</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="post-margin support-me">
            <p><b>❤️ Is this article helpful?</b></p>
            <p>
              <a href="https://www.buymeacoffee.com/hegerdes"
                >Buy me a coffee☕</a
              >,
              <a href="https://paypal.me/hegerdes?country.x=DE&locale.x=de_DE"
                >PayPal me</a
              >
              or support this space to keep it 🖖 and ad-free.
            </p>
            <p>If you can't, do send some 💖 or help to share this article.</p>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "IndexPage",
  data() {
    return {
      running: false,
      video_found: false,
      error: false,
      slugs: [],
      url: "",
      video: "",
      backend: process.env.BACKEND_URL,
    };
  },
  methods: {
    async genereteDownloadURL() {
      try {
        this.running = true;
        this.error = false;
        const formdata = new FormData();
        formdata.append("url", this.url);

        const requestOptions = {
          method: "POST",
          body: formdata,
          redirect: "follow",
        };

        const api_res = await fetch(this.backend, requestOptions);
        const res = await api_res.json();
        this.video_found = true;
        console.log(res);
        this.video = res["download"];
      } catch (err) {
        this.error = true;
      }
      this.running = false;
    },
    async DownloadVid() {
      // const res = await fetch(this.backend + this.url);
      // console.log(this.backend + this.url);
      // const blob = new Blob([await res.blob()], { type: "video/mp4" });
      // const link = document.createElement("a");
      // link.href = URL.createObjectURL(blob);
      // link.click();
      window.open(this.backend + "/" + this.video, "_blank");
    },
  },
};
</script>
