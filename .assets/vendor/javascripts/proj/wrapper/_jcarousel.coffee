((window, ProJ, $) ->
  'use strict'


  mask = (obj) -> (obj.data('size') or '192x192').split 'x'


  carousel = (obj, options) ->
    outer = obj.find('.outer')

    outer.on 'jcarousel:reload jcarousel:create', ->
      el = $ @
      width = el.innerWidth()
      numb = 1
      for w, n of options.width when w < width
        numb = n
      el.jcarousel('items').css 'width', Math.ceil(width / numb - options.margin) + 'px'

    ProJ::lazyload outer, event: 'jcarousel:animateend'

    outer.jcarousel
      wrap: options.wrap
      center: options.center
      animation:
        duration: options.duration
        easing: options.easing

    data = obj.attr 'data-autoscroll'
    data = if interval? then parseInt data else options.autoscroll
    if data
      outer.jcarouselAutoscroll
        interval: data
        target: '+=1'
        autostart: yes

    ctrl = obj.find '.control'
    data = obj.attr 'data-control'
    data = if interval? then parseInt data else options.control
    if data
      el = $('<div/>').addClass 'prev icon'
      ctrl.append el
      el.jcarouselControl target: '-=1'
      el = $('<div/>').addClass 'next icon'
      ctrl.append el
      el.jcarouselControl target: '+=1'
    data = obj.attr 'data-pagination'
    data = if interval? then parseInt data else options.pagination
    if data
      el = $('<div/>').addClass 'pagination'
      ctrl.append el
      el
      .jcarouselPagination
          item: (page)-> $('<div/>').addClass "icon#{ page is '1' and ' active' or '' }"
      .on 'jcarouselpagination:active', '.icon', ->
        $(@).addClass 'active'
      .on 'jcarouselpagination:inactive', '.icon', ->
        $(@).removeClass 'active'


  dynamic = (obj, options) ->
    inner = obj.find '.inner'
    size = mask obj
    fn = (item)->
      el = $('<canvas/>')
      .addClass 'img-fluid bg-cover center-block'
      .attr 'data-src', item.url
      .attr
          width: size[0]
          height: size[1]
          title: item.name
      el = $('<div/>')
      .addClass 'item card'
      .append el
      inner.append el

    $.getJSON obj.data('carousel'), (data) ->
      inner.empty() if obj.data 'mask'
      fn item for item in data.items
      carousel obj, options


  ProJ::jcarousel = (target, options) ->
    if $.isPlainObject target
      options = target
      target = null

    target ?= '[data-carousel]'
    target = $ target if not (target instanceof jQuery)

    options = $.extend
      wrap: 'circular'
      center: no
      duration: 700
      easing: 'easeOutSine',
      autoscroll: 5000
      control: yes
      pagination: yes
      width: null
      margin: 0
      options

    if target.length
      ProJ.link 'css/jcarousel.css'

      target.each ->
        obj = $ @
        outer = obj.find('.outer')
        if not outer.length
          outer = $('<div/>').addClass 'outer'
          obj.append outer
        if not obj.find('.control').length
          outer.before $('<div/>').addClass 'control'
        inner = obj.find('.inner')
        if not inner.length
          inner = $('<div/>').addClass 'inner'
          outer.append inner
        if not inner.html()
          size = mask obj
          inner.append $('<canvas/>').attr
            width: size[0]
            height: size[1]
          obj.data 'mask', yes

      $(window).load ->
        ProJ.script 'js/jcarousel.js', ->
          target.each ->
            obj = $ @
            attr = obj.data 'carousel'
            if attr[0] is '/'
              dynamic obj, options
            else
              carousel obj, options

# ----------------------------------------------------------------------------------------------------

) window, ProJ, jQuery
