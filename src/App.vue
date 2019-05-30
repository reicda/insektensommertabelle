<template>
  <div id="app">
    <v-app>
      <v-card>
        <v-card-title>
          <v-select
            @change="changedAction"
            :items="campains"
            v-model="selectedCampain"
            label="Aktion"
            class="mr-3"
          ></v-select>

          <v-autocomplete
            @change="changeRanking"
            :items="rankings"
            :menu-props="{maxHeight:'700'}"
            v-model="selectedRanking"
            label="Rangliste"
            item-text="name"
            item-value="name"
          >
            <template slot="item" slot-scope="data">
              <template
                id="scroll-target"
                style="max-height: 400px"
                class="scroll-y"
                v-if="typeof data.item !== 'object'"
              >
                <v-list-tile-content v-text="data.item"></v-list-tile-content>
              </template>
              <template v-else>
                <v-list-tile-avatar :tile="true" v-if="data.item.avatar">
                  <img :src="data.item.avatar">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title v-html="data.item.name"></v-list-tile-title>
                  <v-list-tile-sub-title v-html="data.item.group"></v-list-tile-sub-title>
                </v-list-tile-content>
              </template>
            </template>
          </v-autocomplete>

          <v-spacer></v-spacer>

          <v-text-field
            v-model="search"
            append-icon="search"
            label="Suche in Tabelle ..."
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>

        <v-progress-linear slot="progress" color="blue" indeterminate="true"></v-progress-linear>

        <v-data-table
          :disable-initial-sort="true"
          :search="search"
          :headers="headers"
          :items="tableData"
          no-data-text="Keine Daten gefunden."
          hide-actions
          item-key="artname"
          :loading="loading"
          class="elevation-1"
          ref="dTable"
        >
          <template slot="items" slot-scope="props">
            <tr @click="openTChart(props)">
              <td>{{ props.item.rang}}</td>
              <td class="text-xs-left">{{ props.item.artname}}</td>
              <td class="text-xs-left">{{ props.item.meldungen}}</td>
              <td class="text-xs-left">{{ props.item.anzahl}}</td>
              <td class="text-xs-left">{{ props.item.durchschnitt}}</td>
              <td class="text-xs-left">{{ props.item.gattung}}</td>
              <td class="text-xs-left">{{ props.item.taxon}}</td>
            </tr>
          </template>

          <template v-slot:expand="props">
            <Chart :props="props" :value="selectedCampain"></Chart>
          </template>

          <v-alert
            slot="no-results"
            :value="true"
            color="error"
            icon="warning"
          >Leider wurde Dein Suchbegriff "{{ search }}" nicht gefunden.</v-alert>

          <template slot="footer" :items="footer" v-if="footer">
            <td colspan="100%">
              Anzahl Meldungen:
              <strong>{{footer.meldungen}}</strong>
              <br>Anzahl Beobachtungen:
              <strong>{{footer.beobachtungen}}</strong>
            </td>
          </template>
        </v-data-table>
      </v-card>
    </v-app>
  </div>
</template>

<script>
import Chart from "./components/Chart";
import Papa from "papaparse";

function anzahlMeldungen(insekten) {
  var beobachtungen = [];
  insekten.forEach(function(insekt) {
    beobachtungen.push([insekt.lat, insekt.lon]);
  });

  var meldungen = beobachtungen
    .map(JSON.stringify)
    .reverse()
    .filter(function(e, i, a) {
      return a.indexOf(e, i + 1) === -1;
    })
    .reverse()
    .map(JSON.parse);
  return meldungen.length;
}

function anzahlLebensraum(insekten, lebensraum) {
  let beobachtungen = insekten.filter(
    insekt => insekt.lebensraum === lebensraum
  );

  return {
    beobachtungen: beobachtungen.length,
    meldungen: anzahlMeldungen(beobachtungen)
  };
}

function anzahlBundesland(insekten, bundesland) {
  let beobachtungen = insekten.filter(
    insekt => insekt.bundesland === bundesland
  );

  return {
    beobachtungen: beobachtungen.length,
    meldungen: anzahlMeldungen(beobachtungen)
  };
}

function top5bundesland(insekten, bundesland) {
  const bl = insekten.filter(insekt => insekt.bundesland === bundesland);
  const map = new Map();
  bl.forEach(item => {
    const entry = map.get(item.artname);
    if (!entry) {
      map.set(item.artname, {
        artname: item.artname,
        taxon: item.taxon,
        gattung: item.gattung,
        anzahl: Number.parseInt(item.anzahl),
        meldungen: 1
      });
    } else {
      ++entry.meldungen;
      entry.anzahl += Number.parseInt(item.anzahl);
    }
  });
  const top = [...map.values()];
  top.sort(function(a, b) {
    return b.meldungen - a.meldungen;
  });
  let top5 = top.slice(0, 5);
  for (let i = 0; i < top5.length; i++) {
    top5[i].rang = i + 1;
    top5[i].durchschnitt = Number.parseFloat(
      Number.parseInt(top5[i].anzahl) / Number.parseInt(top5[i].meldungen)
    ).toFixed(2);
  }
  return top5;
}

function lebensraumTop5(insekten, lebensraum) {
  const l = insekten.filter(insekt => insekt.lebensraum === lebensraum);
  const map = new Map();
  l.forEach(item => {
    const entry = map.get(item.artname);
    if (!entry) {
      map.set(item.artname, {
        artname: item.artname,
        taxon: item.taxon,
        gattung: item.gattung,
        anzahl: Number.parseInt(item.anzahl),
        meldungen: 1
      });
    } else {
      ++entry.meldungen;
      entry.anzahl += Number.parseInt(item.anzahl);
    }
  });
  const top = [...map.values()];
  top.sort(function(a, b) {
    return b.meldungen - a.meldungen;
  });
  let top5 = top.slice(0, 5);
  for (let i = 0; i < top5.length; i++) {
    top5[i].rang = i + 1;
    top5[i].durchschnitt = Number.parseFloat(
      Number.parseInt(top5[i].anzahl) / Number.parseInt(top5[i].meldungen)
    ).toFixed(2);
  }
  return top5;
}

export default {
  name: "app",
  components: {
    Chart
  },
  data() {
    return {
      search: "",
      loading: true,
      footer: {},
      campains: [
        { text: "Juni 2019", value: "2019-06" },
        { text: "August 2018", value: "2018-08" },
        { text: "Juni 2018", value: "2018-06" }
      ],
      headers: [
        { text: "Rang", value: "rang" },
        { text: "Insektenart", value: "artname" },
        { text: "Meldungen", value: "meldungen" },
        { text: "Anzahl", value: "anzahl" },
        { text: "Individuen pro Meldung", value: "durchschnitt" },
        { text: "Gattung", value: "gattung" },
        { text: "Taxon", value: "taxon" }
      ],
      insects: [],
      tableData: [],
      top100: [],
      selectedRanking: { name: "Top 100" },
      selectedCampain: { text: "Juni 2019", value: "2019-06" },
      rankings: [
        { header: "Ranglisten" },
        { name: "Top 100", avatar: "images/brd.svg" },
        { divider: true },
        { header: "TOP5 Bundesländer" },
        { name: "Baden-Württemberg", avatar: "images/bw.svg" },
        { name: "Bayern", avatar: "images/by.svg" },
        { name: "Brandenburg & Berlin", avatar: "images/bb_be.svg" },
        { name: "Hessen", avatar: "images/he.svg" },
        { name: "Mecklenburg-Vorpommern", avatar: "images/mv.svg" },
        { name: "Niedersachsen & Bremen", avatar: "images/ni_hb.svg" },
        { name: "Nordrhein-Westfalen", avatar: "images/nw.svg" },
        { name: "Rheinland-Pfalz", avatar: "images/rp.svg" },
        { name: "Saarland", avatar: "images/sl.svg" },
        { name: "Sachsen", avatar: "images/sn.svg" },
        { name: "Sachsen-Anhalt", avatar: "images/st.svg" },
        {
          name: "Schleswig-Holstein & Hamburg",
          avatar: "images/sh_hh.svg"
        },
        { name: "Thüringen", avatar: "images/th.svg" },
        { divider: true },
        { header: "TOP5 Lebensraum" },
        { name: "Garten" },
        { name: "Balkon" },
        { name: "Park" },
        { name: "Wiese" },
        { name: "Wald" },
        { name: "Feld" },
        { name: "Teich" },
        { name: "Bach/Fluss" },
        { name: "Sonstiges" }
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
  },
  mounted: function() {
    this.loadData();
  },
  methods: {
    loadData() {
      this.tableData = [];
      this.insects = [];
      this.loading = true;
      fetch("/data/beobachtungen-" + this.selectedCampain.value + ".csv")
        .then(response => response.text())
        .then(data => {
          var results = Papa.parse(data, { header: true });
          this.insects = results.data;
          this.processData();
        });
    },
    processData() {
      const unique = new Map();
      this.insects.forEach(item => {
        const entry = unique.get(item.artname);
        if (!entry) {
          unique.set(item.artname, {
            artname: item.artname,
            taxon: item.taxon,
            gattung: item.gattung,
            anzahl: Number.parseInt(item.anzahl),
            meldungen: 1
          });
        } else {
          ++entry.meldungen;
          entry.anzahl += Number.parseInt(item.anzahl);
        }
      });
      const top = [...unique.values()];
      top.sort(function(a, b) {
        return b.meldungen - a.meldungen;
      });

      const top100 = top.slice(0, 100);
      for (let i = 0; i < top100.length; i++) {
        top100[i].rang = i + 1;
        top100[i].durchschnitt = Number.parseFloat(
          Number.parseInt(top100[i].anzahl) /
            Number.parseInt(top100[i].meldungen)
        ).toFixed(2);
      }
      this.tableData = top100;
      this.top100 = top100;
      this.footer = {
        beobachtungen: this.insects.length - 1,
        meldungen: anzahlMeldungen(this.insects) - 1
      };
      this.loading = false;
    },
    openTChart: function(props) {
      // TODO: Fix if other rankings are implemented!
      if (this.selectedRanking.name === "Top 100") {
        props.expanded = !props.expanded;
      }
    },
    changedAction: function(value) {
      //close all expanded slots
      for (let i = 0; i < this.tableData.length; i += 1) {
        const item = this.tableData[i];
        this.$set(this.$refs.dTable.expanded, item.artname, false);
      }
      this.tableData = [];
      this.selectedRanking = { name: "Top 100" };
      this.selectedCampain = this.campains.find(o => o.value == value);
      this.loadData();
    },
    changeRanking: function(value) {
      this.tableData = [];
      if (value === "Top 100") {
        this.tableData = this.top100;
        //this.footer = {
        //  meldungen: 2760,
        //  beobachtungen: 23739
        //};
        // TODO: Fix reporting of 23740 entries(beobachtungen). Should be 23739. Because 1st must be the header. Strange
        this.footer = {
          beobachtungen: this.insects.length - 1,
          meldungen: anzahlMeldungen(this.insects) - 1
        };
      } else if (
        [
          "Garten",
          "Balkon",
          "Park",
          "Wiese",
          "Wald",
          "Feld",
          "Teich",
          "Bach/Fluss",
          "Sonstiges"
        ].includes(value)
      ) {
        if (value === "Garten") {
          this.tableData = lebensraumTop5(this.insects, value);
          this.footer = anzahlLebensraum(this.insects, value);
        } else {
          this.tableData = lebensraumTop5(this.insects, " " + value);
          this.footer = anzahlLebensraum(this.insects, " " + value);
        }
      } else {
        this.tableData = top5bundesland(this.insects, value);
        this.footer = anzahlBundesland(this.insects, value);
      }
      //close all expanded slots
      for (let i = 0; i < this.tableData.length; i += 1) {
        const item = this.tableData[i];
        this.$set(this.$refs.dTable.expanded, item.artname, false);
      }
    }
  }
};
</script>

<style>
.datatable thead {
  background-color: #c3daea !important;
}

th:hover {
  color: black !important;
}

tr:hover {
  background-color: #e1eef4 !important;
}

.avatar img {
  border-radius: 0%;
}

.white--text.card {
  background-color: #0168b3 !important;
}

th.column:nth-child(5) {
  white-space: pre-wrap;
}
</style>
