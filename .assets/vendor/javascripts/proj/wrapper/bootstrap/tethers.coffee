((window, ProJ, $) ->
  'use strict'

  $ ->
    tooltips = $ '[data-toggle*="tooltip"], .hastip'
    popovers = $ '[data-toggle*="popover"], .haspop'

    if tooltips.length or popovers.length
      ProJ.link 'css/tethers.css'

      ProJ.script 'js/tethers.js', ->
        tooltips.tooltip
          html: yes
          show: 500
          hide: 100
        popovers.popover
          html: yes
          show: 500
          hide: 100

# ----------------------------------------------------------------------------------------------------

) window, ProJ, jQuery
