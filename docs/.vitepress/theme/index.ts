import DefaultTheme from 'vitepress/theme'
import StepPlayer from './StepPlayer.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('StepPlayer', StepPlayer)
  },
}
