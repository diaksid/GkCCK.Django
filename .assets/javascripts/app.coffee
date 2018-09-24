((window, document, screen, location, ProJ, $) ->
  'use strict'


  DEBUG = yes
  MOSAIC_BASE = 300

  ProJ.debug = DEBUG
  ProJ.assets = '//web.gkcck.ru/assets'

  $win = $ window
  $banner = $ '#banner'
  $navbar = $ '#navbar'

  aligns = ->
    ProJ('.aligns')
    .aligns('.align')
    .aligns('.item')

  mosaic = ->
    $('.mosaic').each ->
      self = $ @
      base = self.data('base') or MOSAIC_BASE
      val = 0
      self.find('.frame')
      .each ->
        $(@).height ''
      .each ->
        height = $(@).outerHeight()
        val = height if height < val or not val
      .each ->
        self = $ @
        self.height val * self.prop('height') / base

  host = location.hostname
  path = location.pathname
  home = path is '/' and host is 'dev.gkcck.ru'
  page = (path isnt '/' or host isnt 'dev.gkcck.ru') and path isnt '/contact'
  size = switch
    when screen.width > 1600 then 'xl'
    when screen.width > 1200 then 'lg'
    else
      'sm'


  $ ->
    (new WOW offset: 0).init()

    aligns()
    mosaic()

    ProJ
    .lazyload()
    .mailto()
    .scroll()
    .lightbox()

    ProJ('a.is-active, .is-active > a').deactive()
    ProJ('[data-w3c]').w3c()
    ProJ('[data-ymet]').ymet()

    if home
      $banner.bgswitcher
        duration: 1000
        interval: 15000
        images: [
          "#{ ProJ.assets }/img/bg/home/#{ size }/00.jpg"
          "#{ ProJ.assets }/img/bg/home/#{ size }/01.jpg"
        ]
        shuffle: no
    else if not page
      ProJ.ymaps('.ymap',
        behaviors: [
          'drag'
          'dblClickZoom'
          'rightMouseButtonMagnifier'
          'multiTouch'
        ]
        controls: []
      )


  $win.load ->
    if page
      $banner.bgswitcher
        duration: 1000
        interval: 10000
        images: switch host
          when 'uor.gkcck.ru'
            [
              "#{ ProJ.assets }/img/bg/page/#{ size }/10.jpg"
              "#{ ProJ.assets }/img/bg/page/#{ size }/11.jpg"
              "#{ ProJ.assets }/img/bg/page/#{ size }/12.jpg"
              "#{ ProJ.assets }/img/bg/page/#{ size }/13.jpg"
            ]
          else
            [
              "#{ ProJ.assets }/img/bg/page/#{ size }/00.jpg"
              "#{ ProJ.assets }/img/bg/page/#{ size }/01.jpg"
              "#{ ProJ.assets }/img/bg/page/#{ size }/02.jpg"
            ]
        shuffle: yes
      ProJ.script 'js/canvas/grid.js', -> ProJ.canvasGrid $banner
      ProJ.ymaps('.ymap')
      $banner.find('h1').addClass 'gradient-bottom'

    # if home
    #   ProJ.script 'js/canvas/snow.js', -> ProJ.canvasSnow $banner

    if home or page
      $navbar.addClass 'gradient-top'
      $('.preloader').fadeOut 'slow'


  $win.resize ->
    aligns()
    mosaic()


  $win.scroll ->
    if screen.width > 767
      fix = $navbar.find '.collapse'
      fix = fix.hasClass('collapsing') or fix.hasClass('in')
      if $win.scrollTop() > 96
        if not $navbar.hasClass 'navbar-fixed'
          if fix
            $navbar.addClass 'navbar-fixed'
          else
            $navbar.hide ->
              $navbar
              .addClass 'navbar-fixed'
              .slideDown 200
      else
        if $navbar.hasClass 'navbar-fixed'
          if fix
            $navbar.removeClass 'navbar-fixed'
          else
            $navbar.slideUp 200, ->
              $navbar
              .removeClass 'navbar-fixed'
              .fadeIn 500

# ----------------------------------------------------------------------------------------------------

)(window, document, screen, location, ProJ, jQuery)
