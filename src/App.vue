<template>
  <v-app>
    <TheTable />
  </v-app>
</template>

<script>
import TheTable from "./components/TheTable";
export default {
  name: "App",
  components: {
    TheTable
  },
  data: () => ({
    //
  })
};
</script>