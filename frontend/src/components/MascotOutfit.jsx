import outfits from "../assets/outfits"

const COSTUME_MAP = {
    0: outfits.hello,
    1: outfits.darthVader,
    2: outfits.gladiator,
    3: outfits.chef,
    4: outfits.godfather,
    5: outfits.maradona,
    6: outfits.ferrari,
    7: outfits.barista,
    8: outfits.masked,
    9: outfits.mario,
    10: outfits.davinci,
    11: outfits.biker,
    12: outfits.juliusCaesar,
    13: outfits.columbus, 
    14: outfits.boxer,
    15: outfits.alpineMaid,
    16: outfits.midnightElegance,
    17: outfits.renessainceLady,
    18: outfits.retroDiva,
    19: outfits.sicilianBelle,
    20: outfits.venetianMasquerade
};

export default function Mascot({ costumeId = 0, ...props }) {
    const currentMascotImg = COSTUME_MAP[costumeId];

    return <img src={currentMascotImg} alt="Mascot" {...props} />;
}
