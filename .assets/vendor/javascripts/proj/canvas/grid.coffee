((window, document, ProJ, $) ->
  'use strict'

  CANVAS_RATE = 10
  CANVAS_CORNERS = 5

  $win = $ window

  distance = (p1, p2) -> Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2)


  class Circle

    constructor: (@pos, @rad) ->

    draw: (ctx) ->
      if @active
        ctx.beginPath()
        ctx.arc @pos.x, @pos.y, @rad, 0, Math.PI * 2, no
        ctx.fillStyle = "rgba(255, 255, 255, #{ @active })"
        ctx.fill()


  class Tween

    constructor: (@point) ->

    animate: (del, x, y, cb) ->
      @time = 0
      @del =
        x: if @point.x < x then del else -del
        y: if @point.y < y then del else -del
      @x = x
      @y = y
      @cb = cb
      @frame()

    frame: =>
      if ++@time % 3 is 0
        if @del.x and Math.abs(@x - @point.x) > Math.abs(@del.x)
          @point.x += @del.x
        else
          @del.x = no
        if @del.y and Math.abs(@y - @point.y) > Math.abs(@del.y)
          @point.y += @del.y
        else
          @del.y = no
      if @del.x or @del.y
        ProJ.animation.request @frame
      else
        @cb()


  class Grid

    constructor: (@obj) ->
      @animated = yes
      @canvas = document.createElement 'canvas'
      @obj.append $(@canvas).css
        display: 'block'
        position: 'absolute'
        zIndex: -1
        top: 0
        left: 0
      @ctx = @canvas.getContext '2d'
      @resize()
      @target =
        x: @canvas.width / 2
        y: @canvas.height / 2
      @points = []
      step = switch
        when @canvas.width >= 1200
          x: @canvas.width / CANVAS_RATE
          y: @canvas.height / CANVAS_RATE
        when @canvas.width >= 768
          x: @canvas.width / CANVAS_RATE / .75
          y: @canvas.height / CANVAS_RATE / .75
        else
          x: @canvas.width / CANVAS_RATE / .5
          y: @canvas.height / CANVAS_RATE / .5
      for x in [0...@canvas.width] by step.x
        for y in [0...@canvas.height] by step.y
          _x = Math.random() * step.x + x
          _y = Math.random() * step.y + y
          @points.push
            x: _x
            originX: _x
            y: _y
            originY: _y
      for p1 in @points
        p1.closest = []
        for p2 in @points when p2 isnt p1
          placed = no
          for k in [0...CANVAS_CORNERS] when not placed
            if not p1.closest[k]?
              p1.closest[k] = p2;
              placed = yes
          for k in [0...CANVAS_CORNERS] when not placed
            if distance(p1, p2) < distance(p1, p1.closest[k])
              p1.closest[k] = p2;
              break
      for p in @points
        p.shape = new Circle p, Math.random() * 2 + 2
        p.tween = new Tween p
      @listeners()
      @animate()

    listeners: ->
      $win.on 'mousemove', @mouseMove if not ('ontouchstart' of window)
      $win
      .on 'scroll', @scrollCheck
      .on 'resize', @resize

    mouseMove: (event) =>
      @target = switch
        when event.pageX or event.pageY
          x: event.pageX
          y: event.pageY
        when event.clientX or event.clientY
          x: e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft
          y: e.clientY + document.body.scrollTop + document.documentElement.scrollTop
        else
          x: @canvas.width / 2
          y: @canvas.height / 2

    scrollCheck: =>
      @animated = $win.scrollTop() < @canvas.height

    resize: =>
      @canvas.width = @obj.innerWidth()
      @canvas.height = @obj.innerHeight()

    animate: ->
      @frame()
      @shift p for p in @points

    frame: =>
      if @animated
        @ctx.clearRect 0, 0, @canvas.width, @canvas.height
        for p in @points
          dist = Math.abs distance @target, p
          switch
            when dist < 4000
              p.active = .4
              p.shape.active = .8
            when dist < 10000
              p.active = .3
              p.shape.active = .6
            when dist < 15000
              p.active = .2
              p.shape.active = .4
            when dist < 20000
              p.active = .1
              p.shape.active = .3
            when dist < 40000
              p.active = .03
              p.shape.active = .1
            else
              p.active = 0
              p.shape.active = 0
          if p.active
            for c in p.closest
              @ctx.beginPath()
              @ctx.moveTo p.x, p.y
              @ctx.lineTo c.x, c.y
              @ctx.strokeStyle = "rgba(255, 255, 255, #{ p.active })"
              @ctx.stroke()
          p.shape.draw @ctx
      ProJ.animation.request @frame

    shift: (p) =>
      p.tween.animate 1 + 1 * Math.random(), \
        Math.random() * 100 + p.originX - 50, \
        Math.random() * 100 + p.originY - 50, \
        => @shift p


  ProJ.canvasGrid = (target) -> new Grid target

# ----------------------------------------------------------------------------------------------------

)(window, document, ProJ, jQuery)
