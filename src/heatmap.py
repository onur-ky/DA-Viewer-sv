from src.coverage_df import coverage_df_gen


def heatmap_gen(data):
    df = coverage_df_gen(data)
    hm = df.style.background_gradient(cmap='Blues')
    rendered_table = hm.render()
    # reactify and seperate html and css
    html = rendered_table.split('</style>')[1].replace('<style type="text/css">', '')
    css = rendered_table.split('</style>')[0]
    return html, css
