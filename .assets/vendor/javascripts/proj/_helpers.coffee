((window, ProJ, $) ->
  'use strict'


  $.extend ProJ,
    to: (data) ->
      if data and not (data instanceof ProJ)
        ProJ data
      else data

    to$: (data) ->
      if data and not (data instanceof jQuery)
        jQuery data
      else data

    hexRgb: (hex) ->
      if hex.length is 4
        hex = hex.replace /^#?([a-f\d])([a-f\d])([a-f\d])$/i,
          (match, r, g, b) -> "#{ r }#{ r }#{ g }#{ g }#{ b }#{ b }"
      rgb = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec hex
      if rgb
        r: parseInt rgb[1], 16
        g: parseInt rgb[2], 16
        b: parseInt rgb[3], 16
      else null

# ----------------------------------------------------------------------------------------------------

) window, ProJ, jQuery
