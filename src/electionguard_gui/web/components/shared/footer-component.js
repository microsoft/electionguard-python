export default {
  data() {
    return {
      version: null,
    };
  },
  async mounted() {
    this.version = await eel.get_version()();
  },
  template: /*html*/ `
  <nav class="navbar fixed-bottom bg-light">
    <div class="container">
        <div class="col-12 pe-0 text-end text-secondary text-opacity-75" v-if="version">
          ElectionGuard version {{version}}
        </div>
    </div>
  </nav>
  `,
};
