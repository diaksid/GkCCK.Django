((window, document, ProJ, $) ->
  'use strict'


  class Redactor

    constructor: (@asset, options) ->
      if $.isPlainObject @asset
        options = @asset
        @asset = null

      @options = $.extend
        lang: 'ru'
        minHeight: 160
        maxHeight: 640
        structure: yes
        formatting: ['p', 'blockquote', 'pre']
        buttons: [
          'undo', 'redo'
          'formatting'
          'bold', 'italic', 'underline', 'deleted'
          'alignment'
          'outdent', 'indent'
          'unorderedlist', 'orderedlist'
        ]
        plugins: [
          'fullscreen'
        ]
      , options

      @


    load: ->
      @target = $ '[data-redactor]'
      if @target.length
        if @asset?
          ProJ.script @asset
          @asset = null
        @loader()

      ProJ
      

    loader: =>
      if $.Redactor?
        for el in @target
          $.Redactor el, @options
          delete el.dataset.redactor
      else
        setTimeout @loader, 60


  ProJ.redactor = (asset, options) -> (ProJ.Redactor ?= new Redactor asset, options).load()

# ----------------------------------------------------------------------------------------------------

) window, document, ProJ, jQuery
