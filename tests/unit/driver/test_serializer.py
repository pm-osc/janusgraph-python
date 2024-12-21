from janusgraph_python.driver.serializer import JanusGraphSONSerializersV3d0, JanusGraphBinarySerializersV1
from janusgraph_python.structure.io import graphsonV3d0, graphbinaryV1


def test_graphson_serializer_v3():
    graphson_serializer_v3 = JanusGraphSONSerializersV3d0()
    
    assert graphson_serializer_v3.version == b"application/vnd.gremlin-v3.0+json"
    assert isinstance(graphson_serializer_v3._graphson_reader, graphsonV3d0.JanusGraphSONReader)
    assert isinstance(graphson_serializer_v3.standard._writer, graphsonV3d0.JanusGraphSONWriter)
    assert isinstance(graphson_serializer_v3.traversal._writer, graphsonV3d0.JanusGraphSONWriter)

def test_graphbinary_serializer_v1():
    graphbinary_serializer_v1 = JanusGraphBinarySerializersV1()

    assert graphbinary_serializer_v1.version == b"application/vnd.graphbinary-v1.0"
    assert isinstance(graphbinary_serializer_v1._graphbinary_reader, graphbinaryV1.JanusGraphBinaryReader)
    assert isinstance(graphbinary_serializer_v1.standard._writer, graphbinaryV1.JanusGraphBinaryWriter)
    assert isinstance(graphbinary_serializer_v1.traversal._writer, graphbinaryV1.JanusGraphBinaryWriter)