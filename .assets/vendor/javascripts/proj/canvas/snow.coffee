((window, ProJ, $) ->
  'use strict'

  CANVAS_RATE = 4

  win = $ window


  class Snow

    constructor: (@obj) ->
      @animated = yes
      @canvas = document.createElement 'canvas'
      @obj.append $(@canvas).css
        display: 'block'
        position: 'absolute'
        zIndex: -1
        top: 0
        left: 0
      @resize()
      @ctx = @canvas.getContext '2d'
      maxp = Math.round @canvas.width / CANVAS_RATE
      @particles = for i in [0...maxp]
        x: Math.random() * @canvas.width
        y: Math.random() * @canvas.height
        o: Math.random() * 4 + 1
        r: Math.random() + 1
        d: Math.random() * maxp
      @count = @angle = 0
      @listeners()
      @animate()

    listeners: ->
      win
      .on 'scroll', @scrollCheck
      .on 'resize', @resize

    scrollCheck: =>
      @animated = win.scrollTop() < @canvas.height

    resize: =>
      @canvas.width = @obj.innerWidth()
      @canvas.height = @obj.innerHeight()

    animate: =>
      if @animated and ++@count % 3 is 0
        @ctx.clearRect 0, 0, @canvas.width, @canvas.height
        for p in @particles
          @ctx.beginPath()
          @ctx.fillStyle = "rgba(240, 255, 255, #{ p.o / 10 })"
          @ctx.moveTo p.x, p.y
          @ctx.arc p.x, p.y, p.r, 0, Math.PI * 2, yes
          @ctx.fill()
        @update()
      ProJ.animation.request @animate

    update: =>
      @angle += 0.01
      for p, i in @particles
        p.y += Math.cos(@angle + p.d) + 1 + p.r / 2
        p.x += Math.sin(@angle) * 2
        if p.x > @canvas.width + 5 or p.x < -5 or p.y > @canvas.height
          if i % 3 > 0
            p.x = Math.random() * @canvas.width
            p.y = -10
          else
            p.x = if Math.sin(@angle) > 0 then -5 else @canvas.width + 5
            p.y = Math.random() * @canvas.height
        if @count % 9 is 0
          p.o = Math.random() * 4 + 1


  ProJ.canvasSnow = (target) -> Snow target

# ----------------------------------------------------------------------------------------------------

)(window, ProJ, jQuery)
