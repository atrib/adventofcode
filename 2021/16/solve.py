class Packet():
    version = None
    type = None
    literal = None
    subpackets = None

    def __repr__(self):
        return '({}, {}, {})'.format(self.version,
                                    self.type,
                                    self.literal if self.literal is not None else self.subpackets)

def hex2bits(c):
    mapping = {
        '0': [0, 0, 0, 0],
        '1': [0, 0, 0, 1],
        '2': [0, 0, 1, 0],
        '3': [0, 0, 1, 1],
        '4': [0, 1, 0, 0],
        '5': [0, 1, 0, 1],
        '6': [0, 1, 1, 0],
        '7': [0, 1, 1, 1],
        '8': [1, 0, 0, 0],
        '9': [1, 0, 0, 1],
        'A': [1, 0, 1, 0],
        'B': [1, 0, 1, 1],
        'C': [1, 1, 0, 0],
        'D': [1, 1, 0, 1],
        'E': [1, 1, 1, 0],
        'F': [1, 1, 1, 1]
    }
    return mapping[c]

def bits2int(bits):
    val = 0
    for bit in bits:
        val = 2*val + bit
    return val

def interpret(bits):
    pkt_version = bits2int(bits[:3])
    pkt_type = bits2int(bits[3:6])
    if pkt_type == 4: # Handle literal
        idx = 6
        literal = 0
        while bits[idx] == 1:
            literal = 16*literal + bits2int(bits[idx + 1: idx + 5])
            idx += 5
        literal = 16*literal + bits2int(bits[idx + 1: idx + 5])
        idx += 5

        p = Packet()
        p.version = pkt_version
        p.type = pkt_type
        p.literal = literal
        return (idx, p)
    else: # Handle operator
        pkt_type_id = bits[6]
        if pkt_type_id == 0: # Count bits
            num_subpacket_bits = bits2int(bits[7: 7 + 15])
            subpackets = []
            subpacket_idx = 22
            while subpacket_idx < 22 + num_subpacket_bits:
                (idx, packet) = interpret(bits[subpacket_idx:])
                subpacket_idx += idx
                subpackets.append(packet)
            assert subpacket_idx == 22 + num_subpacket_bits
        else: # Count packets
            num_sub_packets = bits2int(bits[7:7 + 11])
            subpackets = []
            subpacket_idx = 18
            for _ in range(num_sub_packets):
                (idx, packet) = interpret(bits[subpacket_idx:])
                subpacket_idx += idx
                subpackets.append(packet)
            
        p = Packet()
        p.version = pkt_version
        p.type = pkt_type
        p.subpackets = subpackets   

        return (subpacket_idx, p)
        

def create_packet(inp):
    bits = [bit for c in inp for bit in hex2bits(c)]
    # print(bits)
    (idx, packet) = interpret(bits)
    return packet

def count_versions(packet):
    versionsum = packet.version
    subpackets = packet.subpackets
    if subpackets is not None:
        versionsum += sum([count_versions(subpacket) for subpacket in subpackets])
    return versionsum 

inputs = [
    'D2FE28', 
    '38006F45291200',
    'EE00D40C823060',
    '8A004A801A8002F478',
    '620080001611562C8802118E34',
    'C0015000016115A2E0802F182340',
    'A0016C880162017C3686B18A3D4780',
    'E20D72805F354AE298E2FCC5339218F90FE5F3A388BA60095005C3352CF7FBF27CD4B3DFEFC95354723006C401C8FD1A23280021D1763CC791006E25C198A6C01254BAECDED7A5A99CCD30C01499CFB948F857002BB9FCD68B3296AF23DD6BE4C600A4D3ED006AA200C4128E10FC0010C8A90462442A5006A7EB2429F8C502675D13700BE37CF623EB3449CAE732249279EFDED801E898A47BE8D23FBAC0805527F99849C57A5270C064C3ECF577F4940016A269007D3299D34E004DF298EC71ACE8DA7B77371003A76531F20020E5C4CC01192B3FE80293B7CD23ED55AA76F9A47DAAB6900503367D240522313ACB26B8801B64CDB1FB683A6E50E0049BE4F6588804459984E98F28D80253798DFDAF4FE712D679816401594EAA580232B19F20D92E7F3740D1003880C1B002DA1400B6028BD400F0023A9C00F50035C00C5002CC0096015B0C00B30025400D000C398025E2006BD800FC9197767C4026D78022000874298850C4401884F0E21EC9D256592007A2C013967C967B8C32BCBD558C013E005F27F53EB1CE25447700967EBB2D95BFAE8135A229AE4FFBB7F6BC6009D006A2200FC3387D128001088E91121F4DED58C025952E92549C3792730013ACC0198D709E349002171060DC613006E14C7789E4006C4139B7194609DE63FEEB78004DF299AD086777ECF2F311200FB7802919FACB38BAFCFD659C5D6E5766C40244E8024200EC618E11780010B83B09E1BCFC488C017E0036A184D0A4BB5CDD0127351F56F12530046C01784B3FF9C6DFB964EE793F5A703360055A4F71F12C70000EC67E74ED65DE44AA7338FC275649D7D40041E4DDA794C80265D00525D2E5D3E6F3F26300426B89D40094CCB448C8F0C017C00CC0401E82D1023E0803719E2342D9FB4E5A01300665C6A5502457C8037A93C63F6B4C8B40129DF7AC353EF2401CC6003932919B1CEE3F1089AB763D4B986E1008A7354936413916B9B080'
]

for inp in inputs:
    packet = create_packet(inp)
    print(packet)
    count = count_versions(packet)

    print('Sum of version numbers for {} is {}'.format(inp, count))
