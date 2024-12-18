# Copyright 2023 JanusGraph-Python Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from aenum import Enum
from gremlin_python.statics import ListType
from gremlin_python.structure.io.graphbinaryV1 import (
	_GraphBinaryTypeIO, EdgeIO, StringIO, GraphBinaryReader, GraphBinaryWriter,
    int32_pack, uint64_pack, int8_pack, _make_packer,
    uint8_pack, DataType
)
from gremlin_python.structure.graph import Edge, Vertex
from janusgraph_python.process.traversal import _JanusGraphP, RelationIdentifier

uint16_pack, uint16_unpack = _make_packer('>H')
uint32_pack, uint32_unpack = _make_packer('>I')

class JanusGraphDataType(Enum):
    janusgraphp = (0x1002, "janusgraph.P")
    janusgraphrelationidentifier = (0x1001, "janusgraph.RelationIdentifier")

class JanusGraphBinaryReader(GraphBinaryReader):
    def __init__(self):
        # register JanusGraph-specific RelationIdentifier deserializer
        deserializer_map = {
            #JanusGraphDataType.janusgraphrelationidentifier: JanusGraphRelationIdentifierIO
        }
        GraphBinaryReader.__init__(self, deserializer_map)

class JanusGraphBinaryWriter(GraphBinaryWriter):
    def __init__(self):
        # register JanusGraph-specific RelationIdentifier and text-predicate serializer
        serializer_map = [
            #(RelationIdentifier, JanusGraphRelationIdentifierIO),
            (_JanusGraphP, JanusGraphPSerializer)
        ]
        GraphBinaryWriter.__init__(self, serializer_map)


class JanusGraphPSerializer(_GraphBinaryTypeIO):
    graphbinary_type_id = JanusGraphDataType.janusgraphp.value[0]
    graphbinary_type_name = JanusGraphDataType.janusgraphp.value[1]
    python_type = _JanusGraphP

    @classmethod
    def dictify(cls, obj, writer, to_extend, as_value=False, nullable=True):
        if to_extend is None:
            to_extend = bytearray()

        # Part 1: serializing the custom JanusGraph type
        # use the custom type code
        if not as_value:
            to_extend += uint8_pack(DataType.custom.value)

        # add the name of the custom JanusGraph type
        StringIO.dictify(cls.graphbinary_type_name, writer, to_extend, True, False)

        # add the id of the custom JanusGraph type
        to_extend += uint32_pack(cls.graphbinary_type_id)

        # Part 2: serializing the custom JanusGraph operator
        # use the custom type code
        if not as_value:
            to_extend += uint8_pack(DataType.custom.value)

        # serialize the operator
        StringIO.dictify(obj.operator, writer, to_extend, True, False)
        
        # serialize the value
        writer.to_dict(obj.value, to_extend)

        return to_extend

# class JanusGraphRelationIdentifierIO(_GraphBinaryTypeIO):
#     graphbinary_type = JanusGraphDataType.janusgraphrelationidentifier
#     python_type = RelationIdentifier

#     @classmethod
#     def objectify(cls, buff, reader, nullable=True):
#         return cls.is_null(buff, reader, cls._read_edge, nullable)

#     @classmethod
#     def _read_edge(cls, b, r):
#         edgeid = r.read_object(b)
#         edgelbl = r.to_object(b, DataType.string, False)
#         inv = Vertex(r.read_object(b), r.to_object(b, DataType.string, False))
#         outv = Vertex(r.read_object(b), r.to_object(b, DataType.string, False))
#         b.read(2)
#         props = r.read_object(b)
#         # null properties are returned as empty lists
#         properties = [] if props is None else props
#         edge = Edge(edgeid, outv, edgelbl, inv, properties)
#         return edge

#     @classmethod
#     def objectify(cls, l, reader):    
#         return RelationIdentifier.from_string(l['relationId'])
    


#     @classmethod
#     def dictify(cls, relation_identifier, writer):
#         out = { "relationId": relation_identifier.string_representation }
#         return GraphSONUtil.typed_value("RelationIdentifier", out, "janusgraph")
