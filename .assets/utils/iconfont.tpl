$icon-class-iclude: true !default;

<% _.each(glyphs, function(glyph) { %>
@mixin <%= cssClass %>-<%= glyph.fileName %>() {
  &:before {
    content: "\<%= glyph.codePoint %>";
  }
}
<% }); %>

@if $icon-class-iclude {
<% _.each(glyphs, function(glyph) { %>
.<%= cssClass %>-<%= glyph.fileName %> {
  &:before {
    content: "\<%= glyph.codePoint %>";
  }
}
<% }); %>
}
