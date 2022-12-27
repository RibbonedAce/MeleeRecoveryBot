from melee.enums import Action, Button, Character

from Chains.Abstract import RecoveryChain
from Utils import Trajectory, TrajectoryFrame as TF, Vector2, Vector2 as V2
from Utils.enums import LEDGE_GRAB_MODE


class AirDodge(RecoveryChain):
    CPTFALCON_AIR_DODGE = Trajectory(Character.CPTFALCON, 0, 30, LEDGE_GRAB_MODE.AFTER, False, [
        TF.angle(2.79, V2(2.19198, 1.71249)),
        TF.multiply(0.9, V2(2.70766, 1.5205)),
        TF.multiply(0.9, V2(3.9936, 1.59842)),
        TF.multiply(0.9, V2(3.54239, 1.89676)),
        TF.multiply(0.9, V2(3.45259, 2.04046)),
        TF.multiply(0.9, V2(3.46316, 2.03664)),
        TF.multiply(0.9, V2(3.48, 2.02148)),
        TF.multiply(0.9, V2(3.49724, 1.99609)),
        TF.multiply(0.9, V2(3.5085, 1.96184)),
        TF.multiply(0.9, V2(3.50733, 1.92019)),
        TF.multiply(0.9, V2(3.49551, 1.87271)),
        TF.multiply(0.9, V2(3.48064, 1.82096)),
        TF.multiply(0.9, V2(3.46339, 1.76649)),
        TF.multiply(0.9, V2(3.44328, 1.71077)),
        TF.multiply(0.9, V2(3.42102, 1.65517)),
        TF.multiply(0.9, V2(3.39732, 1.60093)),
        TF.multiply(0.9, V2(3.37299, 1.54913)),
        TF.multiply(0.9, V2(3.34883, 1.50069)),
        TF.multiply(0.9, V2(3.32508, 1.45579)),
        TF.multiply(0.9, V2(3.30103, 1.41393)),
        TF.multiply(0.9, V2(3.27614, 1.37497)),
        TF.multiply(0.9, V2(3.24992, 1.339)),
        TF.multiply(0.9, V2(3.22189, 1.30637)),
        TF.multiply(0.9, V2(3.19158, 1.27773)),
        TF.multiply(0.9, V2(3.15862, 1.25412)),
        TF.multiply(0.9, V2(3.15876, 1.24512)),
        TF.multiply(0.9, V2(3.14336, 1.25249)),
        TF.multiply(0.9, V2(3.08965, 1.26246)),
        TF.multiply(0.9, V2(2.92751, 1.24179)),
        TF.drift(Character.CPTFALCON, V2(3.10285, 1.18593)),
        TF.drift(Character.CPTFALCON, V2(3.78826, 1.01859)),
        TF.drift(Character.CPTFALCON, V2(4.04064, 0.78171)),
        TF.drift(Character.CPTFALCON, V2(3.74718, 0.68125)),
        TF.drift(Character.CPTFALCON, V2(4.35537, 0.66297)),
        TF.drift(Character.CPTFALCON, V2(4.34483, 0.70879)),
        TF.drift(Character.CPTFALCON, V2(4.54382, 0.7792)),
        TF.drift(Character.CPTFALCON, V2(5.48604, 0.88132)),
        TF.drift(Character.CPTFALCON, V2(6.77667, 1.37548)),
        TF.drift(Character.CPTFALCON, V2(7.20824, 1.15218)),
        TF.drift(Character.CPTFALCON, V2(7.25941, 0.88259)),
        TF.drift(Character.CPTFALCON, V2(7.32811, 0.90241)),
        TF.drift(Character.CPTFALCON, V2(7.47852, 1.2359)),
        TF.drift(Character.CPTFALCON, V2(7.64001, 1.5895)),
        TF.drift(Character.CPTFALCON, V2(7.91261, 1.98573)),
        TF.drift(Character.CPTFALCON, V2(8.02165, 1.857)),
        TF.drift(Character.CPTFALCON, V2(7.8098, 1.82112)),
        TF.drift(Character.CPTFALCON, V2(7.51936, 1.96707)),
        TF.drift(Character.CPTFALCON, V2(7.44695, 2.13247)),
        TF.drift(Character.CPTFALCON, V2(4.49938, 2.28119))
    ])

    FOX_AIR_DODGE = Trajectory(Character.FOX, 0, 30, LEDGE_GRAB_MODE.AFTER, False, [
        TF.angle(2.79, V2(2.16457, 3.92442)),
        TF.multiply(0.9, V2(2.11403, 4.33013)),
        TF.multiply(0.9, V2(2.41695, 4.77219)),
        TF.multiply(0.9, V2(3.13535, 5.18834)),
        TF.multiply(0.9, V2(2.65207, 5.39219)),
        TF.multiply(0.9, V2(2.69824, 5.47057)),
        TF.multiply(0.9, V2(2.76934, 5.56145)),
        TF.multiply(0.9, V2(2.84549, 5.66789)),
        TF.multiply(0.9, V2(2.9234, 5.79243)),
        TF.multiply(0.9, V2(3.00013, 5.93674)),
        TF.multiply(0.9, V2(3.0728, 6.10121)),
        TF.multiply(0.9, V2(3.13826, 6.28493)),
        TF.multiply(0.9, V2(3.19395, 6.48557)),
        TF.multiply(0.9, V2(3.23783, 6.69954)),
        TF.multiply(0.9, V2(3.26857, 6.89984)),
        TF.multiply(0.9, V2(3.28562, 6.80956)),
        TF.multiply(0.9, V2(3.28922, 6.71882)),
        TF.multiply(0.9, V2(3.2804, 6.62864)),
        TF.multiply(0.9, V2(3.26072, 6.54002)),
        TF.multiply(0.9, V2(3.26341, 6.45395)),
        TF.multiply(0.9, V2(3.29191, 6.37136)),
        TF.multiply(0.9, V2(3.31947, 6.2932)),
        TF.multiply(0.9, V2(3.34464, 6.22032)),
        TF.multiply(0.9, V2(3.36732, 6.15352)),
        TF.multiply(0.9, V2(3.37624, 6.09354)),
        TF.multiply(0.9, V2(3.36275, 5.56469)),
        TF.multiply(0.9, V2(3.64342, 5.39853)),
        TF.multiply(0.9, V2(3.35376, 5.74801)),
        TF.multiply(0.9, V2(3.20874, 5.72249)),
        TF.drift(Character.FOX, V2(3.32557, 5.93006)),
        TF.drift(Character.FOX, V2(3.59736, 6.35366)),
        TF.drift(Character.FOX, V2(3.64653, 6.82127)),
        TF.drift(Character.FOX, V2(3.45615, 6.36771)),
        TF.drift(Character.FOX, V2(3.10432, 5.61677)),
        TF.drift(Character.FOX, V2(2.81667, 5.18551)),
        TF.drift(Character.FOX, V2(2.85881, 5.09885)),
        TF.drift(Character.FOX, V2(3.00355, 4.93224)),
        TF.drift(Character.FOX, V2(2.92956, 4.39032)),
        TF.drift(Character.FOX, V2(2.72097, 3.82962)),
        TF.drift(Character.FOX, V2(2.40062, 3.47238)),
        TF.drift(Character.FOX, V2(2.26466, 3.40495)),
        TF.drift(Character.FOX, V2(2.04891, 3.28926)),
        TF.drift(Character.FOX, V2(2, 2.99635)),
        TF.drift(Character.FOX, V2(2, 2.21033)),
        TF.drift(Character.FOX, V2(2, 1.10444)),
        TF.drift(Character.FOX, V2(2.00203, 0.45174)),
        TF.drift(Character.FOX, V2(2.24104, 0.24745)),
        TF.drift(Character.FOX, V2(2.35607, 0.22292)),
        TF.drift(Character.FOX, V2(2.52219, 0.29744))
    ])

    FALCO_AIR_DODGE = Trajectory(Character.FALCO, 0, 30, LEDGE_GRAB_MODE.AFTER, False, [
        TF.angle(2.79, V2(2.48025, 4.49483)),
        TF.multiply(0.9, V2(2.42232, 4.9565)),
        TF.multiply(0.9, V2(2.6713, 5.46427)),
        TF.multiply(0.9, V2(3.59258, 5.94646)),
        TF.multiply(0.9, V2(3.03883, 6.18312)),
        TF.multiply(0.9, V2(3.09119, 6.27349)),
        TF.multiply(0.9, V2(3.17378, 6.37852)),
        TF.multiply(0.9, V2(3.26144, 6.50174)),
        TF.multiply(0.9, V2(3.35108, 6.64609)),
        TF.multiply(0.9, V2(3.4393, 6.81344)),
        TF.multiply(0.9, V2(3.52273, 7.00423)),
        TF.multiply(0.9, V2(3.59773, 7.21733)),
        TF.multiply(0.9, V2(3.66305, 7.44995)),
        TF.multiply(0.9, V2(3.76377, 7.69785)),
        TF.multiply(0.9, V2(3.85439, 7.89222)),
        TF.multiply(0.9, V2(3.93426, 7.78791)),
        TF.multiply(0.9, V2(4.00364, 7.68351)),
        TF.multiply(0.9, V2(4.06356, 7.58025)),
        TF.multiply(0.9, V2(4.11572, 7.4793)),
        TF.multiply(0.9, V2(4.16215, 7.38182)),
        TF.multiply(0.9, V2(4.20547, 7.28889)),
        TF.multiply(0.9, V2(4.24918, 7.20156)),
        TF.multiply(0.9, V2(4.29091, 7.12077)),
        TF.multiply(0.9, V2(4.33015, 7.04739)),
        TF.multiply(0.9, V2(4.35334, 6.98218)),
        TF.multiply(0.9, V2(4.20048, 6.48795)),
        TF.multiply(0.9, V2(4.16304, 6.22487)),
        TF.multiply(0.9, V2(4.02241, 6.0375)),
        TF.multiply(0.9, V2(3.81269, 5.75291)),
        TF.drift(Character.FALCO, V2(3.8335, 5.95455)),
        TF.drift(Character.FALCO, V2(3.94944, 6.53748)),
        TF.drift(Character.FALCO, V2(4.38557, 7.85526)),
        TF.drift(Character.FALCO, V2(4.40381, 8.34714)),
        TF.drift(Character.FALCO, V2(4.05082, 7.27694)),
        TF.drift(Character.FALCO, V2(3.70259, 6.55734)),
        TF.drift(Character.FALCO, V2(3.61841, 6.27119)),
        TF.drift(Character.FALCO, V2(3.67048, 5.88859)),
        TF.drift(Character.FALCO, V2(3.47167, 5.05809)),
        TF.drift(Character.FALCO, V2(3.05985, 4.24657)),
        TF.drift(Character.FALCO, V2(2.68229, 3.72496)),
        TF.drift(Character.FALCO, V2(2.29235, 3.57172)),
        TF.drift(Character.FALCO, V2(2, 3.40918)),
        TF.drift(Character.FALCO, V2(2, 3.04416)),
        TF.drift(Character.FALCO, V2(2, 2.31472)),
        TF.drift(Character.FALCO, V2(2.25421, 1.33933)),
        TF.drift(Character.FALCO, V2(2.8172, 0.76454)),
        TF.drift(Character.FALCO, V2(3.0238, 0.60799)),
        TF.drift(Character.FALCO, V2(3.05401, 0.58041)),
        TF.drift(Character.FALCO, V2(3.09125, 0.56492))
    ])

    GANONDORF_AIR_DODGE = Trajectory(Character.GANONDORF, 0, 30, LEDGE_GRAB_MODE.AFTER, False, [
        TF.angle(2.79, V2(2.59177, 1.77899)),
        TF.multiply(0.9, V2(3.17982, 1.62711)),
        TF.multiply(0.9, V2(4.78549, 1.76878)),
        TF.multiply(0.9, V2(4.75771, 2.13547)),
        TF.multiply(0.9, V2(4.58875, 2.29307)),
        TF.multiply(0.9, V2(4.60837, 2.27891)),
        TF.multiply(0.9, V2(4.60377, 2.26287)),
        TF.multiply(0.9, V2(4.58016, 2.23947)),
        TF.multiply(0.9, V2(4.53546, 2.20339)),
        TF.multiply(0.9, V2(4.47477, 2.15581)),
        TF.multiply(0.9, V2(4.41235, 2.10234)),
        TF.multiply(0.9, V2(4.34711, 2.04436)),
        TF.multiply(0.9, V2(4.27515, 1.98326)),
        TF.multiply(0.9, V2(4.19736, 1.92037)),
        TF.multiply(0.9, V2(4.11468, 1.85699)),
        TF.multiply(0.9, V2(4.02805, 1.79435)),
        TF.multiply(0.9, V2(3.93848, 1.73355)),
        TF.multiply(0.9, V2(3.84703, 1.6756)),
        TF.multiply(0.9, V2(3.75473, 1.62136)),
        TF.multiply(0.9, V2(3.66266, 1.57159)),
        TF.multiply(0.9, V2(3.5708, 1.52602)),
        TF.multiply(0.9, V2(3.47823, 1.48399)),
        TF.multiply(0.9, V2(3.39172, 1.44572)),
        TF.multiply(0.9, V2(3.3662, 1.41172)),
        TF.multiply(0.9, V2(3.33957, 1.38282)),
        TF.multiply(0.9, V2(3.36385, 1.36635)),
        TF.multiply(0.9, V2(3.38365, 1.36165)),
        TF.multiply(0.9, V2(3.37138, 1.35452)),
        TF.multiply(0.9, V2(3.26395, 1.3142)),
        TF.drift(Character.GANONDORF, V2(3.80246, 1.23733)),
        TF.drift(Character.GANONDORF, V2(4.48754, 1.06043)),
        TF.drift(Character.GANONDORF, V2(4.79173, 0.84507)),
        TF.drift(Character.GANONDORF, V2(4.52046, 0.78)),
        TF.drift(Character.GANONDORF, V2(4.09344, 0.77279)),
        TF.drift(Character.GANONDORF, V2(3.69267, 0.83317)),
        TF.drift(Character.GANONDORF, V2(3.93455, 0.91995)),
        TF.drift(Character.GANONDORF, V2(6.39376, 1.07628)),
        TF.drift(Character.GANONDORF, V2(7.77193, 1.57231)),
        TF.drift(Character.GANONDORF, V2(8.21386, 1.24905)),
        TF.drift(Character.GANONDORF, V2(8.28296, 0.8745)),
        TF.drift(Character.GANONDORF, V2(8.37049, 0.77017)),
        TF.drift(Character.GANONDORF, V2(8.54539, 1.03821)),
        TF.drift(Character.GANONDORF, V2(8.81359, 1.23709)),
        TF.drift(Character.GANONDORF, V2(9.12193, 1.51423)),
        TF.drift(Character.GANONDORF, V2(9.25282, 1.86319)),
        TF.drift(Character.GANONDORF, V2(9.02305, 1.81719)),
        TF.drift(Character.GANONDORF, V2(8.72926, 1.91005)),
        TF.drift(Character.GANONDORF, V2(8.56718, 1.98293)),
        TF.drift(Character.GANONDORF, V2(8.73237, 2.02636))
    ])

    MARTH_AIR_DODGE = Trajectory(Character.MARTH, 0, 30, LEDGE_GRAB_MODE.AFTER, False, [
        TF.angle(2.79, V2(2, 3.76448)),
        TF.multiply(0.9, V2(2, 4.37263)),
        TF.multiply(0.9, V2(2, 5.42067)),
        TF.multiply(0.9, V2(2, 6.24982)),
        TF.multiply(0.9, V2(2.22662, 6.33721)),
        TF.multiply(0.9, V2(3.10381, 6.00069)),
        TF.multiply(0.9, V2(3.46051, 6.0021)),
        TF.multiply(0.9, V2(3.57051, 6.05722)),
        TF.multiply(0.9, V2(3.66461, 6.07413)),
        TF.multiply(0.9, V2(3.74475, 6.08877)),
        TF.multiply(0.9, V2(3.8142, 6.10115)),
        TF.multiply(0.9, V2(3.8757, 6.11132)),
        TF.multiply(0.9, V2(3.93005, 6.1193)),
        TF.multiply(0.9, V2(3.9782, 6.12518)),
        TF.multiply(0.9, V2(4.02125, 6.12904)),
        TF.multiply(0.9, V2(4.06059, 6.13098)),
        TF.multiply(0.9, V2(4.09734, 6.13111)),
        TF.multiply(0.9, V2(4.13162, 6.12955)),
        TF.multiply(0.9, V2(4.16291, 6.12642)),
        TF.multiply(0.9, V2(4.19032, 6.12186)),
        TF.multiply(0.9, V2(4.21287, 6.11597)),
        TF.multiply(0.9, V2(4.22979, 6.10891)),
        TF.multiply(0.9, V2(4.24031, 6.10078)),
        TF.multiply(0.9, V2(4.2431, 6.09173)),
        TF.multiply(0.9, V2(4.23645, 6.08188)),
        TF.multiply(0.9, V2(4.22857, 6.07135)),
        TF.multiply(0.9, V2(4.2309, 6.06025)),
        TF.multiply(0.9, V2(4.21719, 6.04871)),
        TF.multiply(0.9, V2(4.1833, 6.0296)),
        TF.drift(Character.MARTH, V2(4.12436, 5.98564)),
        TF.drift(Character.MARTH, V2(4.03466, 5.92956)),
        TF.drift(Character.MARTH, V2(3.90764, 5.87265)),
        TF.drift(Character.MARTH, V2(3.73591, 5.7548)),
        TF.drift(Character.MARTH, V2(3.51316, 5.53437)),
        TF.drift(Character.MARTH, V2(3.45133, 5.28874)),
        TF.drift(Character.MARTH, V2(3.4908, 5.03344)),
        TF.drift(Character.MARTH, V2(3.49956, 4.78318)),
        TF.drift(Character.MARTH, V2(3.50227, 4.56495)),
        TF.drift(Character.MARTH, V2(3.33868, 4.40279)),
        TF.drift(Character.MARTH, V2(2.95024, 4.31704)),
        TF.drift(Character.MARTH, V2(2.41998, 4.26154)),
        TF.drift(Character.MARTH, V2(2, 4.17542)),
        TF.drift(Character.MARTH, V2(2, 4.05763)),
        TF.drift(Character.MARTH, V2(2, 3.91158)),
        TF.drift(Character.MARTH, V2(2.0195, 3.74443)),
        TF.drift(Character.MARTH, V2(2.07544, 3.56619)),
        TF.drift(Character.MARTH, V2(2.09326, 3.35744)),
        TF.drift(Character.MARTH, V2(2.08983, 3.19041)),
        TF.drift(Character.MARTH, V2(2.0806, 3.0801))
    ])

    TRAJECTORY_DICTIONARY = {Character.CPTFALCON: CPTFALCON_AIR_DODGE,
                             Character.FOX: FOX_AIR_DODGE,
                             Character.FALCO: FALCO_AIR_DODGE,
                             Character.GANONDORF: GANONDORF_AIR_DODGE,
                             Character.MARTH: MARTH_AIR_DODGE}

    @classmethod
    def create_trajectory(cls, character):
        return AirDodge.TRAJECTORY_DICTIONARY[character]

    def step_internal(self, propagate):
        smashbot_state = propagate[1]

        # We're done here if...
        if self.current_frame > 0 and smashbot_state.action not in self._applicable_states():
            return False

        # If we haven't started yet, hit the input
        if self.current_frame < 0 and smashbot_state.action not in self._applicable_states():
            return self._input_move(Button.BUTTON_L, Vector2(0, 1))

        self._increment_current_frame(smashbot_state)

        # Deciding if we should fade-back
        if self.current_frame > 0:
            if self.current_frame == 1:
                self.controller.release_button(Button.BUTTON_L)
                self.trajectory = self.create_trajectory(smashbot_state.character)

            self._perform_fade_back(propagate)

        self.interruptable = False
        return True

    def _applicable_states(self):
        return {Action.AIRDODGE, Action.DEAD_FALL}