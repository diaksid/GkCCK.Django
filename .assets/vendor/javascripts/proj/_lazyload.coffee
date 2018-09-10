((window, document, ProJ, $) ->
  'use strict'


  class Lazy

    constructor: (@el, @options) ->
      @obj = $(@el).on 'lazyload', @appear
      @opacity = @obj.data("#{ @options.attribute }-opacity") or 1
      @appearance = @opacity * ProJ.animation.delay / (@obj.data("#{ @options.attribute }-duration") or @options.duration)
      @delay = @obj.data("#{ @options.attribute }-delay") or @options.delay
      @

    appear: =>
      if not @above() and not @below() and not @right() and not @left()
        @options.before?.call @obj
        @loader()
        @obj.off 'lazyload'

    loader: ->
      data = @el.dataset[@options.attribute]
      if @options.mask
        if @el.tagName is 'IMG'
          @el.src = @options.mask
        else
          @el.style.backgroundImage = "url(\"#{ @options.mask }\")"
      img = new Image()
      img.onload = =>
        @el.style.opacity = 0
        if @el.tagName is 'IMG'
          @el.src = data
        else
          @el.style.backgroundImage = "url(#{ data })"
        if @delay >= ProJ.animation.delay
          ProJ.animation.request @wait
        else
          ProJ.animation.request @animate
      img.src = data

    above: ->
      value = switch
        when @options.scope?
          @options.scope.offset().top
        else
          window.pageYOffset
      value >= @obj.outerHeight() + @obj.offset().top + @options.threshold

    below: ->
      value = switch
        when @options.scope?
          @options.scope.innerHeight() + @options.scope.offset().top
        else
          window.innerHeight + window.pageYOffset
      value <= @obj.offset().top - @options.threshold

    right: ->
      value = switch
        when @options.scope?
          @options.scope.innerWidth() + @options.scope.offset().left
        else
          window.innerWidth + window.pageXOffset
      value <= @obj.offset().left - @options.threshold

    left: ->
      value = switch
        when @options.scope?
          @options.scope.offset().left
        else
          window.pageXOffset
      value >= @obj.outerWidth() + @obj.offset().left + @options.threshold

    wait: =>
      @delay -= ProJ.animation.delay
      if @delay >= ProJ.animation.delay
        ProJ.animation.request @wait
      else
        ProJ.animation.request @animate

    animate: =>
      @el.style.opacity = parseFloat(@el.style.opacity) + @appearance
      if @opacity - @el.style.opacity >= @appearance
        ProJ.animation.request @animate
      else
        @el.style.opacity = @opacity
        @options.after?.call @obj


  class Lazyload

    constructor: (options) ->
      @default = $.extend
        scope: null
        threshold: 0
        attribute: 'lazy'
        event: 'scroll'
        duration: ProJ.animation.duration
        delay: 0
        before: null
        after: null
        mask: "data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Crect fill='#acc' fill-opacity='.2' height='100%' width='100%'/%3E%3C/svg%3E"
      , options
      @

    load: (selector, options) ->
      if $.isPlainObject selector
        options = selector
        selector = null
      @options = $.extend {}, @default, options
      @options.scope = ProJ.to$ @options.scope
      @container = ProJ.to$ selector
      @target = $ "[data-#{ @options.attribute }]", @container
      @items = []
      for item in @target
        item = new Lazy item, @options
        @items.push item if not item.appear()
      if @items.length
        if @container
          @container.on @options.event, @update
        else
          window.addEventListener @options.event, @update
        window.addEventListener 'resize', @update
      ProJ

    update: =>
      counter = 0
      for item, idx in @items when item?
        if item.appear() then delete @items[idx]
        else counter++
      if counter is 0
        if @container
          @container.off @options.event, @update
        else
          window.removeEventListener @options.event, @update
        window.removeEventListener 'resize', @update

    reset: ->
      if @target
        for item in @target
          if item.tagName is 'IMG'
            item.src = @options.mask
          else
            item.style.backgroundImage = "url(\"#{ @options.mask }\")"


  ProJ.lazyload = (selector, options) -> (ProJ.Lazyload ?= new Lazyload options).load(selector, options)

# ----------------------------------------------------------------------------------------------------

) window, document, ProJ, jQuery
