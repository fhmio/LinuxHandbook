import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import './style.css'

import Breadcrumbs from './components/Breadcrumbs.vue'
import Pagination from './components/Pagination.vue'
import ArticleCard from './components/ArticleCard.vue'
import CheatsheetCard from './components/CheatsheetCard.vue'
import ToolCard from './components/ToolCard.vue'
import SeriesCard from './components/SeriesCard.vue'
import HorizontalArticleItem from './components/HorizontalArticleItem.vue'
import CustomHome from './components/CustomHome.vue'
import LinuxCommandsView from './components/LinuxCommandsView.vue'
import BashView from './components/BashView.vue'
import UbuntuView from './components/UbuntuView.vue'
import SeriesView from './components/SeriesView.vue'
import CheatsheetsView from './components/CheatsheetsView.vue'
import ToolsView from './components/ToolsView.vue'
import AboutView from './components/AboutView.vue'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('Breadcrumbs', Breadcrumbs)
    app.component('Pagination', Pagination)
    app.component('ArticleCard', ArticleCard)
    app.component('CheatsheetCard', CheatsheetCard)
    app.component('ToolCard', ToolCard)
    app.component('SeriesCard', SeriesCard)
    app.component('HorizontalArticleItem', HorizontalArticleItem)
    app.component('CustomHome', CustomHome)
    app.component('LinuxCommandsView', LinuxCommandsView)
    app.component('BashView', BashView)
    app.component('UbuntuView', UbuntuView)
    app.component('SeriesView', SeriesView)
    app.component('CheatsheetsView', CheatsheetsView)
    app.component('ToolsView', ToolsView)
    app.component('AboutView', AboutView)
  }
}
