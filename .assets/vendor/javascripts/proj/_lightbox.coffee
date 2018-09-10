((window, document, ProJ, $) ->
  'use strict'


  class Lightbox

    constructor: (options) ->
      @default = $.extend
        padding: 0
        show: 250
        hide: 250
        step: 250
      , options

      @overlay = $('<div/>')
      .addClass 'lightbox-overlay'
      .hide()
      .on 'click', => @hide()

      el = $('<div/>')
      .addClass 'lightbox-wrapper'
      .prependTo @overlay

      @content = $('<div/>')
      .addClass 'lightbox-content'
      .on 'click', (event) -> event.stopPropagation()
      .prependTo el

      @next = $('<div/>')
      .addClass 'lightbox-next'
      .on 'click', => @step yes
      .prependTo @content

      @prev = $('<div/>')
      .addClass 'lightbox-prev'
      .on 'click', => @step()
      .prependTo @content

      @close = $('<div/>')
      .addClass 'lightbox-close'
      .on 'click', => @hide()
      .prependTo @content

      @

    load: (selector, options) ->
      if $.isPlainObject selector
        options = selector
        selector = null

      @options = $.extend {}, @default, options
      @target = selector or $ '[data-lightbox]'
      @target = $ @target if not (@target instanceof jQuery)

      @stack = {}
      @group = @path = ''
      @item el for el in @target

      @content.css padding: "#{ @options.padding }px" if @options.padding
      @overlay.prependTo $ document.body

      ProJ

    item: (el) ->
      path = el.href or el.dataset.href or el.dataset.lightboxHref
      group = if path[0] is '#' then 'html' else el.dataset.lightbox

      if group and group isnt 'html' and group isnt 'ajax'
        @stack[group] = [] if not @stack[group]?
        @stack[group].push path

      el.addEventListener 'click', (event) =>
        event.preventDefault()
        @path = path
        @group = group
        switch group
          when 'html' then @html()
          else
            @draw()
        no

    html: ->
      @image?.hide()
      @content
      .removeClass 'lightbox-draw'
      .addClass 'lightbox-html'

      @next.hide()
      @prev.hide()

      if not @modal?
        @modal = $('<div/>')
        .addClass 'lightbox-modal'
        .prependTo @content

      @modal.css display: ''
      $el = $ @path
      if $el.length
        @modal.html $el.html()
        @show()

    draw: (step) ->
      @modal?.hide()
      @content
      .removeClass 'lightbox-html'
      .addClass 'lightbox-draw'

      if not @image?
        @image = $('<img/>')
        .addClass 'lightbox-image'
        .prependTo @content

        (fn = => @image?.css maxHeight: "#{ Math.floor window.innerHeight * .95 }px")()
        $(window).resize fn

      if @group and @stack[@group].length > 1
        @next.show()
        @prev.show()
      else
        @next.hide()
        @prev.hide()

      @image
      .attr src: @path
      .css display: ''

      el = @image.get 0
      if el.complete
        @show step
      else
        el.onload = => @show step

    show: (step) ->
      if step
        @content.fadeIn @options.step
      else
        @overlay.fadeIn @options.show

    hide: (cb) ->
      if cb
        @content.fadeOut @options.step, cb
      else
        @overlay.fadeOut @options.show

    step: (next) ->
      idx = @stack[@group].indexOf @path
      if next
        if idx < @stack[@group].length - 1
          ++idx
        else
          idx = 0
      else
        if idx > 0
          --idx
        else
          idx = @stack[@group].length - 1

      @hide =>
        @path = @stack[@group][idx]
        @draw yes


  ProJ.lightbox = (options) -> (ProJ.Lightbox ?= new Lightbox options).load()

# ----------------------------------------------------------------------------------------------------

) window, document, ProJ, jQuery
