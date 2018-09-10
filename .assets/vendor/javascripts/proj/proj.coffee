((window, $) ->
  'use strict'


  init = (selector, context) -> new JPro selector, context


  class ProJ

    @version: '1.2.1'

    @debug: yes
    @assets: ''

    @target: $ document

    @console: (type, message) ->
      if @debug
        if not message?
          message = type
          type = 'log'
      console[type] message
      @

    @asset: (path)->
      path = path.slice(1) if path[0] is '/'
      if not @debug
        path = path.split '.'
        path.splice path.length - 1, 0, 'min'
        path = path.join '.'
      "#{ @assets }/#{ path }"

    @link: (path)->
      path = @asset path if path.indexOf('//') is -1
      $('head').append $('<link/>').attr
        rel: 'stylesheet'
        href: path
      @

    @script: (path, cb)->
      path = @asset path if path.indexOf('//') is -1
      $.ajax
        url: path
        dataType: 'script'
        cache: yes
        success: if cb? then cb
      @

    @find: (selector, context) ->
      context = context.target if context instanceof ProJ
      $ selector, context

    constructor: init

    find: (selector) ->
      @selector = selector if selector?
      @context = @target
      @target = ProJ.find @selector, @context
      @

    each: (callback, args) ->
      @target.each callback, args
      @

    get: (idx = 0) ->
      @target[idx] if 0 <= idx < @target.length


  class JPro extends ProJ

    constructor: (selector, context) ->
      @target = if context? then ProJ.find(context) else ProJ.target
      @find selector


  window.ProJ = ProJ

# ----------------------------------------------------------------------------------------------------

) window, jQuery
