((window, document, ProJ, $) ->
  'use strict'


  ANIMATION_DELAY = 60
  ANIMATION_DURATION = 1000

  $.extend ProJ,
    animation:
      delay: ANIMATION_DELAY
      duration: ANIMATION_DURATION

      request: (callback, el) ->
        delay = @delay
        (
          window.requestAnimationFrame\
            or
            window.webkitRequestAnimationFrame\
            or
            window.mozRequestAnimationFrame\
            or
            window.oRequestAnimationFrame\
            or
            window.msRequestAnimationFrame\
            or
            (callback) ->
              setTimeout callback, delay
        ) callback, el

      cancel: (id) -> (
        window.cancelAnimationFrame\
          or
          window.webkitCancelRequestAnimationFrame\
          or
          window.mozCancelAnimationFrame\
          or
          window.oCancelRequestAnimationFrame\
          or
          window.msCancelRequestAnimationFrame\
          or
          (id) ->
            clearTimeout id
      ) id

    scrolled: -> $ 'html:not(:animated), body:not(:animated)'

    totop: (event) ->
      event.preventDefault()
      ProJ.scrolled().animate scrollTop: 0, ProJ.animation.duration, event.data?.cb
      ProJ

    tobottom: (event) ->
      event.preventDefault()
      ProJ.scrolled().animate scrollTop: $(document).height(), ProJ.animation.duration, event.data?.cb
      ProJ

    toobj: (obj, margin, cb) ->
      obj = $ obj if not (obj instanceof jQuery)
      if typeof margin is 'function'
        cb = margin
        margin = null
      margin ?= 0
      ProJ.scrolled().animate scrollTop: obj.offset().top - margin, ProJ.animation.duration, cb
      ProJ


  $.extend ProJ::,
    totop: (event, cb) ->
      if typeof event is 'function'
        cb = event
        event = null
      event ?= 'click'
      @target.on event, ProJ.totop
      @

    tobottom: (event, cb) ->
      if typeof event is 'function'
        cb = event
        event = null
      event ?= 'click'
      @target.on event, cb: cb, ProJ.tobottom
      @

    toobj: (obj, args...) ->
      event = 'click'
      margin = 0
      cb = null
      for arg in args
        switch typeof arg
          when 'string'
            event = arg
          when 'number'
            margin = arg
          when 'function'
            cb = arg
      @target.on event, (event) ->
        event.preventDefault()
        ProJ.toobj obj, margin, cb
      @

# ----------------------------------------------------------------------------------------------------

) window, document, ProJ, jQuery
