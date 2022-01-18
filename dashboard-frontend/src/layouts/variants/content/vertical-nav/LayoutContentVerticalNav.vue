<template>
  <layout-content-vertical-nav :nav-menu-items="navMenuItems">
    <slot></slot>

    <!-- Slot: Navbar -->
    <template #navbar>
      <div
        class="navbar-content-container"
      >
        <div class="d-flex align-center">
          <v-btn
            small
            color="primary"
            @click="goToAddHousingPage"
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
import { mdiHeartOutline, mdiHomeOutline, mdiMenu } from '@mdi/js'
import LayoutContentVerticalNav from '@/@core/layouts/variants/content/vertical-nav/LayoutContentVerticalNav.vue'

// App Bar Components
import AppBarUserMenu from '@/components/AppBarUserMenu.vue'
import navMainMenuItems from '@/navigation/vertical/main-pages'
import navHousingMenuItems from '@/navigation/vertical/housing-pages'
import navAccountMenuItems from '@/navigation/vertical/account-pages'

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
        housingMenuItems.push(this.housingMenuItem(id, housing))
      })

      return [
        ...navMainMenuItems,
        ...navHousingMenuItems,
        ...housingMenuItems,
        ...navAccountMenuItems,
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
  methods: {
    housingMenuItem(id, housing) {
      return {
        title: housing.name,
        icon: mdiHomeOutline,
        to: { name: 'housing-page', params: { id } },
      }
    },
    goToAddHousingPage: function event() {
      this.$router.push({ name: 'add-housing-page' })
    },
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
