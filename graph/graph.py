from nltk.data import find
import gensim
word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)
print(model.most_similar(positive=['university'], topn = 10))



import networkx as nx
G = nx.star_graph(20)

for v in G.nodes():
    G.nodes[v]['name']=str(v)


from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4



# for start_node, end_node, _ in G.edges(data=True):
#     edge_color = SAME_CLUB_COLOR if G.nodes[start_node]["club"] == G.nodes[end_node]["club"] else DIFFERENT_CLUB_COLOR
#     edge_attrs[(start_node, end_node)] = edge_color
# 
# nx.set_edge_attributes(G, edge_attrs, "edge_color")
# 
# Show with Bokeh
plot = Plot(plot_width=400, plot_height=400,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Graph Interaction Demonstration"
 
node_hover_tool = HoverTool(tooltips=[("name", "@name")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
# 
graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
#graph_renderer.node_renderer.data_source.data['name'] = G.edges
# graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
# graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)
# 
output_file("interactive_graphs.html")
#show(plot)

