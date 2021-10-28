<template>
  <v-card>
    <v-card-title>Configuration</v-card-title>
    <v-simple-table height="400">
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-uppercase">
              Nom
            </th>
            <th class="text-center text-uppercase">
              Périodes
            </th>
            <th class="text-center text-uppercase">
              Prix de base
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="season in seasons"
            :key="season.name"
          >
            <td>{{ season.name }}</td>
            <td class="text-center">
              <p
                v-for="period in season.periods"
                :key="period.start"
              >
                {{ period.start }} - {{ period.end }}
              </p>
            </td>
            <td class="text-center">
              {{ season.base_price }}
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-card>
</template>

<script>
export default {
  setup() {
    const seasons = [
      {
        name: 'basse saison',
        periods: [
          {
            start: '01/01',
            end: '31/03',
          },
          {
            start: '01/11',
            end: '31/12',
          },
        ],
        base_price: 100,
      },
      {
        name: 'moyenne saison',
        periods: [
          {
            start: '01/04',
            end: '31/05',
          },
          {
            start: '01/09',
            end: '31/10',
          },
        ],
        base_price: 120,
      },
      {
        name: 'haute saison',
        periods: [
          {
            start: '01/06',
            end: '31/08',
          },
        ],
        base_price: 140,
      },
    ]

    return {
      seasons,
    }
  },
}
</script>
