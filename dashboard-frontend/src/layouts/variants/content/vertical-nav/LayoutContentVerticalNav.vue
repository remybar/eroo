<template>
  <layout-content-vertical-nav :nav-menu-items="navMenuItems">
    <slot></slot>

    <!-- Slot: Navbar -->
    <template #navbar>
      <div
        class="navbar-content-container"
        :class="{'expanded-search': shallShowFullSearch}"
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
import { mdiMenu, mdiHeartOutline } from '@mdi/js'
import LayoutContentVerticalNav from '@/@core/layouts/variants/content/vertical-nav/LayoutContentVerticalNav.vue'

// App Bar Components
import AppBarUserMenu from '@/components/AppBarUserMenu.vue'
import navMenuItems from '@/navigation/vertical'

export default {
  components: {
    LayoutContentVerticalNav,

    // App Bar Components
    AppBarThemeSwitcher,
    AppBarUserMenu,
  },
  setup() {
    return {
      navMenuItems,
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
