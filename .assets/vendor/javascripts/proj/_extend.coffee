((window, ProJ, $) ->
  'use strict'


  $.extend ProJ,
    aligns: (selector) ->
      val = 0
      (selector instanceof jQuery && selector || $ selector)
      .each ->
        @style.height = ''
        height = $(@).height()
        val = height if height > val
      .each ->
        @style.height = "#{ val }px"
      @

    scroll: (margin, cb) ->
      $('[data-scroll]').on 'click', (event) ->
        event.preventDefault()
        selector = @dataset.scroll or @getAttribute 'href'
        if selector and not @parentNode.classList.contains('is-active') and not @classList.contains('is-active')
          switch selector
            when '#' then ProJ.totop event
            else ProJ.toobj selector, margin, cb
      @

    base64: ->
      $('[data-base64]').each -> @innerHTML += atob @dataset.base64
      @

    mailto: ->
      $('[data-mailto]').each ->
        mail = atob @dataset.mailto
        if mail
          @href = "mailto://#{ mail }"
          @innerHTML += mail if not @dataset.mailtoSafe?
        else
          @style.visibility = 'hidden'
      @

    w3c: ->
      window.open "//validator.w3.org/nu/?doc=#{ encodeURIComponent location.href }&showsource=yes&showoutline=yes",
                  '_blank'
      @

    ymet: ->
      window.open "//metrika.yandex.ru/dashboard?id=#{ @dataset.ymet }",
                  '_blank' if @dataset.ymet
      @



  $.extend ProJ::,
    aligns: (selector) ->
      if selector
        @target.each -> ProJ.aligns $(@).find selector
      else
        ProJ.aligns @target
      @

    deactive: ->
      @target.on 'click', (event) -> event.preventDefault()
      @

    w3c: ->
      @target.on 'click', ProJ.w3c
      @

    ymet: ->
      @target.on 'click', ProJ.ymet
      @

# ----------------------------------------------------------------------------------------------------

) window, ProJ, jQuery
