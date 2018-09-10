((window, ProJ, $) ->
  'use strict'

  carousels = $ '.carousel'

  ProJ.link 'css/carousel.css' if carousels.length


  $ ->
    if carousels.length
      ProJ.script 'js/carousel.js', -> carousels.carousel interval: 7000

# ----------------------------------------------------------------------------------------------------

) window, ProJ, jQuery
