<template>
  <v-card-title>
    <v-select
      v-model="selectedCampain"
      :items="campains"
      label="Aktion"
      class="mr-3"
      return-object
      @change="notifyCampainChange" />


    <v-autocomplete
      v-model="selectedRanking"
      :items="rankings"
      :menu-props="{maxHeight:'700'}"
      label="Rangliste"
      item-text="name"
      item-value="name"
      :hint="`${selectedRanking.group?selectedRanking.group:''}`"
      return-object
      @change="notifyRankingChange">
      <template
        slot="item"
        slot-scope="data">
        <template
          v-if="typeof data.item !== 'object'"
          id="scroll-target"
          style="max-height: 400px"
          class="scroll-y">
          <v-list-item-content v-text="data.item" />
        </template>
        <template v-else>
          <v-list-item-avatar
            v-if="data.item.avatar"
            :tile="true">
            <img
              alt="Flaggen der Bundeslaender"
              :src="data.item.avatar">
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title v-html="data.item.name" />
          </v-list-item-content>
        </template>
      </template>
    </v-autocomplete>

    <v-spacer />

    <v-text-field
      v-model="search"
      append-icon="mdi-magnify"
      label="Suche in Tabelle ..."
      single-line
      hide-details />
  </v-card-title>
</template>

<script>
export default {
  name: "TheTableHeader",
  data() {
    return {
      search: "",
      campains: [
        { text: "August 2019", value: "2019-08" },
        { text: "Juni 2019", value: "2019-06" },
        { text: "August 2018", value: "2018-08" },
        { text: "Juni 2018", value: "2018-06" }
      ],
      selectedRanking: { name: "Top 100" },
      selectedCampain: { text: "August 2019", value: "2019-08" },
      rankings: [
        { header: "Ranglisten" },
        { name: "Top 100", avatar: "images/brd.svg" },
        { divider: true },
        { header: "TOP5 Bundesländer" },
        {
          name: "Baden-Württemberg",
          avatar: "images/bw.svg",
          group: "TOP5 Bundesländer"
        },
        { name: "Bayern", avatar: "images/by.svg", group: "TOP5 Bundesländer" },
        {
          name: "Brandenburg & Berlin",
          avatar: "images/bb_be.svg",
          group: "TOP5 Bundesländer"
        },
        { name: "Hessen", avatar: "images/he.svg", group: "TOP5 Bundesländer" },
        {
          name: "Mecklenburg-Vorpommern",
          avatar: "images/mv.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Niedersachsen & Bremen",
          avatar: "images/ni_hb.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Nordrhein-Westfalen",
          avatar: "images/nw.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Rheinland-Pfalz",
          avatar: "images/rp.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Saarland",
          avatar: "images/sl.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Sachsen",
          avatar: "images/sn.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Sachsen-Anhalt",
          avatar: "images/st.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Schleswig-Holstein & Hamburg",
          avatar: "images/sh_hh.svg",
          group: "TOP5 Bundesländer"
        },
        {
          name: "Thüringen",
          avatar: "images/th.svg",
          group: "TOP5 Bundesländer"
        },
        { divider: true },
        { header: "TOP5 Lebensräume" },
        { name: "Garten", group: "TOP5 Lebensräume" },
        { name: "Balkon", group: "TOP5 Lebensräume" },
        { name: "Park", group: "TOP5 Lebensräume" },
        { name: "Wiese", group: "TOP5 Lebensräume" },
        { name: "Wald", group: "TOP5 Lebensräume" },
        { name: "Feld", group: "TOP5 Lebensräume" },
        { name: "Teich", group: "TOP5 Lebensräume" },
        { name: "Bach/Fluss", group: "TOP5 Lebensräume" },
        { name: "Sonstiges", group: "TOP5 Lebensräume" }
      ]
    };
  },
  created: function() {
    let searchParams = new URLSearchParams(window.location.search);
    let param;
    if (searchParams.has("campain")) {
      param = searchParams.get("campain");
      this.selectedCampain = this.campains.find(o => o.value == param);
    }
    this.notifyCampainChange()
  },
  methods: {
    notifyCampainChange() {
      this.$emit("update:selectedCampain", this.selectedCampain);
    },
    notifyRankingChange(){
      this.$emit("update:selectedRanking", this.selectedRanking);
    }
  }
};
</script>