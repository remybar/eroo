<template>
  <layout-content-vertical-nav :nav-menu-items="navMenuItems">
    <slot></slot>

    <!-- Slot: Navbar -->
    <template #navbar>
      <div
        class="navbar-content-container"
      >
        <!-- Left Content: Search -->
        <div class="d-flex align-center">
          <v-btn
            small
            color="primary"
          >
            Ajouter un logement
          </v-btn>
        </div>

        <!-- Right Content: I18n, Light/Dark, Notification & User Dropdown -->
        <div class="d-flex align-center right-row">
          <app-bar-theme-switcher class="mx-4"></app-bar-theme-switcher>
          <app-bar-user-menu></app-bar-user-menu>
        </div>
      </div>
    </template>

    <!-- Slot: Footer -->
    <template #footer>
      <div class="d-flex justify-space-between">
        <span>contact@eroo.fr</span>
      </div>
    </template>
  </layout-content-vertical-nav>
</template>

<script>
import AppBarThemeSwitcher from '@core/layouts/components/app-bar/AppBarThemeSwitcher.vue'
import { mdiMenu, mdiHeartOutline, mdiHomeOutline } from '@mdi/js'
import LayoutContentVerticalNav from '@/@core/layouts/variants/content/vertical-nav/LayoutContentVerticalNav.vue'

// App Bar Components
import AppBarUserMenu from '@/components/AppBarUserMenu.vue'
import navMainMenuItems from '@/navigation/vertical/main-pages'
import navHousingMenuItems from '@/navigation/vertical/housing-pages'

export default {
  components: {
    LayoutContentVerticalNav,

    // App Bar Components
    AppBarThemeSwitcher,
    AppBarUserMenu,
  },
  computed: {
    navMenuItems() {
      const housingMenuItems = []

      Object.entries(this.$store.state.housings.housings).forEach(([id, housing]) => {
        housingMenuItems.push({
          title: housing.name,
          icon: mdiHomeOutline,
          to: 'second-page',
          children: [
            {
              title: 'Réservations',
              to: `page-${id}`,
            },
            {
              title: 'Site Web',
              to: '',
            },
          ],
        })
      })

      return [
        ...navMainMenuItems,
        ...navHousingMenuItems,
        ...housingMenuItems,
      ]
    },
  },
  setup() {
    return {
      icons: {
        mdiMenu,
        mdiHeartOutline,
      },
    }
  },
}
</script>

<style lang="scss" scoped>
.navbar-content-container {
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-grow: 1;
  position: relative;
}
</style>
