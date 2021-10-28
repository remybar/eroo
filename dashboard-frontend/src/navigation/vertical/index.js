import { mdiHomeOutline, mdiViewDashboardOutline } from '@mdi/js'

export default [
  {
    title: 'Tableau de bord',
    icon: mdiViewDashboardOutline,
    to: 'dashboard',
  },
  {
    title: 'Ajouter logement',
    to: 'add-housing',
  },

  {
    subheader: 'MES LOGEMENTS',
  },
  {
    title: 'Appart Paris',
    icon: mdiHomeOutline,
    to: 'second-page',
    children: [
      {
        title: 'Réservations',
        to: '',
      },
      {
        title: 'Site Web',
        to: '',
      },
    ],
  },
  {
    title: '<Mon Logement>',
    icon: mdiHomeOutline,
    to: 'mon_logement_1',
  },
]
